import os
from copy import deepcopy

import cv2
import numpy as np
from PySide6 import QtCore
from loguru import logger as log

from ..data import DATA, CaptureData
from ..image_process import compare_image
from ..utils import read_numbered_image_names, read_image, save_image


class BuildImageThread(QtCore.QThread):
    """image构建线程"""
    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def main(self) -> None:
        """主函数"""
        data = deepcopy(self.data)  # 深拷贝数据，避免修改原数据
        path = os.path.join(data.score_save_path, data.score_title)

        if not os.path.exists(path):
            log.error(f"指定路径不存在: {path}")
            self.signal_finished.emit()
            return

        # 获取capture图像文件名列表
        file_names = read_numbered_image_names(path, "capture")
        if file_names == []:
            self.signal_finished.emit()
            return

        # 清除旧的image文件
        image_files = read_numbered_image_names(path, "image")
        for f in image_files:
            os.remove(os.path.join(path, f))

        # 获取差异值信息
        if "CaptureData.json" in os.listdir(path):
            capture_data = CaptureData.load_from_file(
                os.path.join(path, "CaptureData.json"))
        else:
            capture_data = CaptureData()
        diff_list: list[float] = []
        captures = [read_image(os.path.join(path, f)) for f in file_names]
        for n in range(len(captures)-1):
            diff = capture_data.get_diff(
                file_names[n], file_names[n+1], data.compare_method)
            if not diff:
                diff = compare_image(cv2.cvtColor(captures[n], cv2.COLOR_RGB2GRAY),
                                     cv2.cvtColor(
                                         captures[n+1], cv2.COLOR_RGB2GRAY),
                                     method=data.compare_method)
                log.debug(
                    f"{data.compare_method}-{file_names[n]}:{file_names[n+1]}-{diff}")
                capture_data.add_diff(
                    file_names[n], file_names[n+1], data.compare_method, diff)
            diff_list.append(diff)
        capture_data.save_to_file(os.path.join(path, "CaptureData.json"))

        # 对图像取平均
        image_count = 0
        if data.compare_method == "SSIM":
            different_index = [
                n+1 for n in range(len(diff_list)) if diff_list[n] < data.compare_threshold]
        elif data.compare_method == "MSE":
            different_index = [
                n+1 for n in range(len(diff_list)) if diff_list[n] > data.compare_threshold]
        else:
            log.error(f"未知的比较方法: {data.compare_method}")
            self.signal_finished.emit()
            return
        different_index.append(0)
        if data.if_keep_last:
            different_index.append(len(diff_list)+1)  # 添加最后一组
        different_index = list(set(different_index))  # 先去重
        different_index.sort()   # 后排序
        image_names_couple = [(file_names[different_index[n]+1],
                              file_names[different_index[n+1]-2])
                              for n in range(len(different_index)-1)]
        log.debug(f"capture_index-{image_names_couple}")
        capture_sequnce = [captures[different_index[n]:different_index[n+1]]
                           for n in range(len(different_index)-1)]
        capture_sequnce = [i for i in capture_sequnce if len(i) > 2]
        image_count = 0
        for sequnce in capture_sequnce:
            image = np.average([np.asarray(i).astype(np.uint16)  # 转换为uint16，避免求和数据溢出
                                for i in sequnce[1:-1]],  # 不要首尾两张
                               axis=0  # 保留图片形状
                               ).astype(np.uint8)  # 转换回图片格式
            save_image(os.path.join(
                path, f"image{image_count}{data.score_save_format}"), image)
            image_count += 1
        log.success("image重构建完成")
        self.signal_finished.emit()

    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"image构建线程异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit()
