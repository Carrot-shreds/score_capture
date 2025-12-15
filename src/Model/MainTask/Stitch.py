import os
from copy import deepcopy

import cv2
import numpy as np
from PySide6 import QtCore
from loguru import logger as log

from ..data import DATA, ScoreDetections, StitchData
from ..image_process import (detect_vertical_lines, detect_horizontal_lines, compare_image,
                            get_barline_num_region, clip_image, stitch_images)
from ..utils import read_numbered_image_names, read_numbered_images, read_image, save_image


class StitchThread(QtCore.QThread):
    """
    图片拼接主进程
    """
    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    @log.catch()
    def main(self) -> None:
        """stitch主函数"""
        data = deepcopy(self.data)
        path = data.working_path
        score_detections = ScoreDetections(path, data.score_title)
        image_files: list[str] = []

        if "ScoreDetections" in os.listdir(path):
            score_detections: ScoreDetections = ScoreDetections.load_from_file(
                os.path.join(path, "ScoreDetections"))
            image_files = score_detections.get_image_filenames()
            log.debug("成功读取缓存，跳过线段检测")
        elif data.stitch_method != "DIRECT":
            # 获取检测数据
            log.info("开始检测图像中的线段")
            for filename in os.listdir(path):
                if filename.rfind("image") >= 0:
                    if filename.rfind("detected") >= 0:  # 移除检测过的图像
                        os.remove(os.path.join(path, filename))
                        continue
                    image_files.append(filename)
                    image_path = os.path.join(path, filename)
                    image = read_image(image_path)
                    image_gray = np.asarray(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
                    horizontal_lines = detect_horizontal_lines(image_gray, data.detect_coefficient_horizontal)
                    vertical_lines = detect_vertical_lines(image_gray, horizontal_lines, data.detect_coefficient_vertical)
                    for line in horizontal_lines:
                        line.draw(image)
                    for line in vertical_lines:
                        line.draw(image)
                    save_filename = filename.split(".")[0] + "-detected" + data.score_save_format
                    save_image(os.path.join(path,save_filename), image)
                    score_detections.add_image(filename, horizontal_lines, vertical_lines)
                    log.debug(
                        f"{filename}-horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
            if len(image_files) < 2:
                log.error("未发2现张或以上可供拼接的图像，请检查文件夹中image数目")
                self.signal_finished.emit()
                return
            score_detections.save_to_file(os.path.join(path, "ScoreDetections"))
            log.info("线段检测完毕，已生成对应预览图")

        # 获取排序后的图片名称
        image_names = read_numbered_image_names(path, "image")
        images = read_numbered_images(path, "image", image_names)
        images_gray:list[np.ndarray] = [np.asarray(cv2.cvtColor(i, cv2.COLOR_RGB2GRAY)) for i in images]

        # 获取mse最低时的拼接像素点
        if data.stitch_method == "DIRECT":
            log.info("直接拼接模式，跳过比对")
            stitch_points = [0] * (len(images) - 1)
        else:
            log.info("比对图片中")
            stitch_points: list[int] = []
            stitch_direction = data.stitch_direction
            # 拼接参考线方向，与拼接方向相反
            if stitch_direction == "vertical":  
                reference_lines_direction = "horizontal"
            elif stitch_direction == "horizontal":
                reference_lines_direction = "vertical"
            # 水平拼接中，获取小节数字序号的区域，以设置权重
            if stitch_direction == "horizontal":  
                barline_num_detect_start, barline_num_detect_end = get_barline_num_region(score_detections[0])
            for name_index in range(len(image_names) - 1):
                img1:np.ndarray = images_gray[name_index]
                img2:np.ndarray = images_gray[name_index + 1]
                length = img1.shape[0] if stitch_direction == "vertical" else img1.shape[1]  # 拼接方向上的长度
                try:
                    line_index = score_detections[image_names[name_index]].get_lines_index(
                        reverse=True, extern_width=2, direction=reference_lines_direction)
                    stitch_indexs = [line_index + line.start_pixel 
                                    for line in score_detections[image_names[name_index+1]].get_lines(
                                        direction=reference_lines_direction)]
                    stitch_indexs = np.unique(np.concatenate(stitch_indexs))  # 拼接成一维数组并进行去重
                    stitch_index:list[int] = list(stitch_indexs[stitch_indexs < length])  # 限定拼接索引区域范围
                except ValueError:
                    stitch_index=[]
                if stitch_index == []:  # 当img1，img2无重合特征线时
                    log.warning(f"{image_names[name_index]}与{image_names[name_index+1]}无重合特征线，"
                                "将在中间区域进行比对")
                    stitch_index = [i for i in range(1,length)]  # stitch_index不能为0!!!
                    stitch_index = stitch_index[int(length*0.2):int(length*0.8)]  # 取中间3/5的区域
                if data.stitch_method == "SSIM":
                    diff = [compare_image(clip_image(img1, stitch_direction, (-offset, None)),
                                        clip_image(img2, stitch_direction, (None, offset)),
                                        "SSIM")
                                    for offset in stitch_index if offset>7]
                    # 在水平模式中，增加小节数字序号区域的权重
                    if stitch_direction == "horizontal":
                        diff = np.asarray(diff)*0.2 + \
                            [compare_image(img1[barline_num_detect_start:barline_num_detect_end, -offset:],
                                            img2[barline_num_detect_start:barline_num_detect_end, :offset],
                                            "SSIM")*0.8
                                for offset in stitch_index if offset>7]  # SSIM算法要求最小图像大小
                    # 右侧1像素为img2的部分，越大越相似
                    stitch_points.append(int(stitch_index[np.argmax(np.asarray(diff))] + 1))
                elif data.stitch_method == "MSE":
                    img1, img2 = np.astype(img1, np.int16), np.astype(img2, np.int16)  # ！！！避免差值数据溢出
                    diff = [np.std(clip_image(img1, stitch_direction, (-offset, None)) - 
                                    clip_image(img2, stitch_direction, (None, offset)))
                            for offset in stitch_index]
                    stitch_points.append(
                        # 同上，diff越小越相似
                        int(stitch_index[np.argmin(np.asarray(diff))] + 1))
                        
                log.debug(f"{stitch_direction}:{data.stitch_method}-"
                        f"{image_names[name_index]}-{image_names[name_index + 1]}"
                        f"-stitch_point:{stitch_points[-1]}")
            log.info("图像比对完毕")

        # 保存拼接点数据
        stitchData = StitchData(stitch_points, images_gray, stitch_direction)
        stitchData.save_to_file(os.path.join(path, "StitchData.json"))

        # 进行拼接
        log.info("图像拼接中")
        final_image = stitch_images(images, stitch_points, data.stitch_direction)
        save_filename = data.score_title + "-stitched" + data.score_save_format
        save_image(os.path.join(data.working_path, save_filename), final_image)
        log.info(f"图像拼接完毕，已生成预览图{os.path.join(data.working_path, save_filename)}")

        self.signal_finished.emit()
        return

    def run(self):
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"拼接线程运行异常: {e}")
        finally:
            self.signal_finished.emit()  # 确保线程结束时发出信号
