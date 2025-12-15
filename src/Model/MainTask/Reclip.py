import os
from copy import deepcopy

import cv2
import numpy as np
from PySide6 import QtCore
from loguru import logger as log

from data import DATA, Line, ScoreDetections
from image_process import detect_all_lines_with_clip
from utils import read_image, save_image


class ReclipThread(QtCore.QThread):
    """
    重分割主进程
    """

    signal_finished = QtCore.Signal()  # 处理完毕信号

    def __init__(self, data: DATA):
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作

    def main(self) -> None:
        """重分割主函数"""
        data = deepcopy(self.data)
        path = data.working_path
        stitched_image_file = data.score_title+"-stitched"+data.score_save_format
        stitched_detected_image_file = data.score_title+"-stitched-detected"+data.score_save_format
        image_path = os.path.join(path, stitched_image_file)

        if stitched_image_file not in os.listdir(path):
            log.error(f"未在当前工作目录下发现{stitched_image_file}图片，请先进行拼接操作")
            self.signal_finished.emit()
            return
        if stitched_detected_image_file in os.listdir(path):  # 移除检测过的图像
            os.remove(os.path.join(path, stitched_detected_image_file))

        # 获取检测数据
        vertical_lines: list[Line] = []
        log.info("开始检测图像中的线段")
        image = read_image(os.path.join(path, stitched_image_file))
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        if "ScoreDetections" in os.listdir(path):
            clip_length = ScoreDetections.load_from_file(
                os.path.join(path, "ScoreDetections"))[0].image_shape[1]
        else:
            clip_length = int(data.SCREEN_SIZE[0]*0.8)
        horizontal_lines, vertical_lines = detect_all_lines_with_clip(image_gray,
                                                                      clip_length,
                                                                      data.detect_coefficient_horizontal,
                                                                      data.detect_coefficient_vertical)
        for line in horizontal_lines:
            line.draw(image)
        for line in vertical_lines:
            line.draw(image)
        save_image(os.path.join(path, stitched_detected_image_file), image)
        log.debug(
            f"horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
        log.info("线段检测完毕，已生成对应预览图")

        # 小节线分组
        index = np.asarray([line.start_pixel for line in vertical_lines])
        distance = index[1:] - index[:-1]
        del_index:list[int] = []
        for i in np.where(distance < np.average(distance)/5)[0]:
            vertical_lines[i].set_thickness(
                vertical_lines[i+1].end_pixel - vertical_lines[i].start_pixel)
            del_index.append(i+1)
        bar_lines = list(np.delete(np.asarray(vertical_lines), del_index))
        image = read_image(image_path)
        image_draw = deepcopy(image)
        for line in bar_lines:
            line.draw(image_draw)
        save_filename = data.score_title + "-detected-barlines" + data.score_save_format
        save_image(os.path.join(path, save_filename) , image_draw)
        log.info(f"成功对小节线进行归类，共检测出{len(bar_lines)}组小节线,预览图像已保存")

        # 进行切片
        log.debug("开始进行切片操作")
        image_clips:list[np.ndarray] = []
        clip_index:list[list[int]] = []
        extern_pixel = 4  # 切片左右额外包含的像素
        if data.reclip_method == 0:  # 每行固定小节数
            each_line_bar_num = 4  # 每行的固定小节数
            for i in range(len(bar_lines)):
                if len(bar_lines) - i <= each_line_bar_num:  # 包含最后一组余数，随后跳出循环
                    clip_index.append([bar_lines[i].start_pixel - extern_pixel,
                                       bar_lines[-1].end_pixel + extern_pixel])
                    break
                elif i % each_line_bar_num == 0:
                    clip_index.append([bar_lines[i].start_pixel - extern_pixel,
                                       bar_lines[i+each_line_bar_num].end_pixel + extern_pixel])
                    if i == len(bar_lines) - 1 - each_line_bar_num:
                        break
        elif data.reclip_method == 1:  # 填充每行最大长度
            bar_lines_index = np.asarray([i.start_pixel for i in bar_lines])
            max_length = bar_lines[4].end_pixel - bar_lines[0].start_pixel  # 使用前四小节的总长度作为限制长度
            result_index = [bar_lines_index[0]]
            for i in range(bar_lines_index.size):
                if bar_lines_index[i]-result_index[-1] >= max_length:
                    # 取i-1,不超过最大长度的部分
                    result_index.append(bar_lines_index[i-1])
            result_index = np.concatenate(  # 图片索引转lines索引
                [np.where(bar_lines_index == i)[0] for i in result_index])
            if result_index[-1] != bar_lines_index.size-1:
                result_index = np.append(result_index, bar_lines_index.size-1)  # 添加入最后一组
            clip_index = [[bar_lines[result_index[i]].start_pixel - extern_pixel,
                           bar_lines[result_index[i+1]].end_pixel + extern_pixel]
                          for i in range(result_index.size-1)]
        for i in clip_index:
            clip_start = max(0, i[0])  # 确保起始位置不小于0
            clip_end = min(image.shape[1], i[1])  # 确保结束位置不大于图片宽度
            image_clips.append(image[:, clip_start:clip_end, :])  # 切片
        log.debug("成功完成切片操作")

        # 拼接
        log.debug("开始进行拼接操作")
        canvas = np.ones_like(image_clips[np.argmax(
            [c.size for c in image_clips])]).astype(np.uint8)*255  # 白色画布
        canvas = np.concatenate([canvas for _ in range(len(image_clips))], axis=0)  # 将画布的高度拓展len(clips)倍
        current_y = 0
        canvas_width = canvas.shape[1]
        for c in image_clips:
            if c.shape[1] != canvas_width:
                c:np.ndarray
                c = cv2.resize(c, (canvas_width, c.shape[0]), 
                               interpolation=cv2.INTER_CUBIC)  # 图像缩放插值方法
            h = c.shape[0]
            w = c.shape[1]
            if data.clip_align == 0:  # 靠左
                canvas[current_y:current_y+h, 0:w, :] = c
            elif data.clip_align == 1:  # 居中
                space = int((canvas_width-w)/2)
                canvas[current_y:current_y+h, space:w+space, :] = c
            elif data.clip_align == 2:  # 靠右
                canvas[current_y:current_y+h,
                       canvas_width-w:canvas_width, :] = c
            current_y += h
        save_filename =  data.score_title + "-reclip" + data.score_save_format
        save_image(os.path.join(path, save_filename), canvas)
        log.success(
            f"拼接操作成功完成，已成功保存图片到{os.path.join(path, save_filename)}"
        )

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()
        except Exception as e:
            log.error(f"重分割线程运行异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit()

