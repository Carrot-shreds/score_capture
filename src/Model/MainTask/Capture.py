import os
import time
import copy

import cv2
import numpy as np
from PySide6 import QtCore
from loguru import logger as log

from ..data import DATA, CaptureData
from ..image_process import image_pre_process, compare_image
from ..utils import save_image, screenshot


class CaptureThread(QtCore.QThread):
    """
    截图主线程
    """
    # 处理完毕信号
    signal_finished = QtCore.Signal()

    def __init__(self, data: DATA) -> None:
        super().__init__()
        self.data: DATA = data
        self.is_working: bool = False  # 主进程是否正在工作
        self.signal_stop: bool = False  # 中止线程信号

    def main(self) -> None:
        """截图主函数"""
        data: DATA = copy.deepcopy(self.data)  # 使用深拷贝，以保证data在执行中不变
        capture_data = CaptureData()
        temp_list: list[np.ndarray] = []
        image_list: list[np.ndarray] = []
        image_count: int = -1  # 去重后输出的单张图像数量
        temp_count: int = -1  # 每轮阈值相同的循环
        total_count: int = -1  # 总截图张数
        time.sleep(0.5)  # 略微延时
        while True:  # 图片截取主循环
            temp_list.append(image_pre_process(
                screenshot(region=data.region.get_tuple(), capture_tool=data.capture_tool
            ), data))
            temp_count += 1
            total_count += 1
            save_filename = f"capture{total_count}{data.score_save_format}"
            save_image(os.path.join(data.working_path, save_filename), temp_list[temp_count])
            if total_count == 0:
                log.info("===开始截图===")
            if temp_count == 0:  # 不过第一张图象不进行对比
                time.sleep(data.capture_delay)  # 延时
                continue

            # 将temp图像与上一张进行对比
            diff = compare_image(cv2.cvtColor(temp_list[temp_count], cv2.COLOR_RGB2GRAY),  # 转换为灰度图
                                 cv2.cvtColor(temp_list[temp_count - 1], cv2.COLOR_RGB2GRAY),
                                 data.compare_method)  # 指定算法
            capture_data.add_diff(  # 保存到数据类
                image1=f"capture{total_count-1}{data.score_save_format}",
                image2=f"capture{total_count}{data.score_save_format}",
                compare_method=data.compare_method,
                diff=diff)
            # 与阈值相比较
            if data.compare_method == "SSIM":
                is_different = diff < data.compare_threshold
            elif data.compare_method == "MSE":
                is_different = diff > data.compare_threshold
            else:
                log.error("未知算法类型")
                self.signal_finished.emit()
                return
            # 输出diff至log
            if is_different:
                log.info(
                    f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
            else:
                log.debug(
                    f"{data.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}")
                
            # 保存去重后的图像
            if is_different or (self.signal_stop and data.if_keep_last):  # 对最后一组进行保留
                if len(temp_list) > 2:  # 只保留缓存图像为三张以上的情况，以消除抖动
                    # 对temp图像取平均值，不计首尾两张，计算时转换格式为uint16，以避免求和数据溢出
                    image: np.ndarray = np.astype(np.average([np.array(i, dtype=np.uint16) for i in temp_list[1:-1]],
                                                             axis=0),  # 延0轴求和，保留图片数组形状
                                                  np.uint8)  # 转换回uint8格式
                    image_list.append(image)
                    image_count += 1
                    save_filename = f"image{image_count}{data.score_save_format}"
                    save_image(os.path.join(data.working_path, save_filename), image)
                    log.success(f"output image{image_count} from "
                                f"capture{total_count - temp_count + 1}-{total_count - 1}")
                temp_list.clear()  # 清除缓存
                temp_count = -1  # 重置计数
            if self.signal_stop:  # 检测信号跳出循环
                self.signal_stop = False
                log.success("===本次截图完成===")
                capture_data.save_to_file(os.path.join(data.working_path, "CaptureData.json"))
                self.signal_finished.emit()
                return
            time.sleep(data.capture_delay)  # 延时


    def run(self) -> None:
        """线程入口启动函数，重写自run方法，使用.start()调用"""
        try:
            self.main()  # 调用主函数
        except Exception as e:
            log.error(f"截图线程异常：{e}")
        finally:  # 确保线程结束时发出信号
            self.signal_finished.emit() 

