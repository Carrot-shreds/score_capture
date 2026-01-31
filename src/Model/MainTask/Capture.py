import os
import time
from pathlib import Path

import cv2
import numpy as np
from PySide6.QtCore import Signal, SignalInstance

from src.Model.Data.data import CaptureData
from src.Model.Data.settings import BuildImageSettings, CaptureSettings
from src.Model.Data.type import Directory, Flag, RegionData
from src.Model.image_process import compare_image, image_pre_process
from src.Model.MainTask.BaseTaskThread import BaseTaskThread
from src.Model.utils import save_image, screenshot


def start_capture_loop(
    captureSettings: CaptureSettings,
    buildImageSettings: BuildImageSettings,
    regionData: RegionData,
    working_dir: Directory,
    stop_flag: Flag,
    logger=None,
    signalBuildImage: SignalInstance | None = None,
) -> None:
    if not logger:
        from loguru import logger as log
    else:
        log = logger
    os.chdir(working_dir)
    log.debug(f"Working dir: {working_dir}")

    captureData = CaptureData()
    temp_list: list[np.ndarray] = []
    image_list: list[np.ndarray] = []
    image_count: int = -1  # 去重后输出的单张图像数量
    temp_count: int = -1  # 每轮阈值相同的循环
    total_count: int = -1  # 总截图张数
    time.sleep(captureSettings.delay_time)  # 略微延时
    while True:  # 图片截取主循环
        temp_list.append(
            image_pre_process(
                screenshot(region_data=regionData, capture_tool=captureSettings.tool),
                captureSettings.if_reverse_image,
            )
        )
        temp_count += 1
        total_count += 1
        save_filename = f"capture{total_count}{captureSettings.save_format}"
        save_image(working_dir / save_filename, temp_list[temp_count])
        if total_count == 0:
            log.info("===开始截图===")
        if temp_count == 0:  # 不过第一张图象不进行对比
            time.sleep(captureSettings.delay_time)  # 延时
            continue

        # 将temp图像与上一张进行对比
        diff = compare_image(
            cv2.cvtColor(temp_list[temp_count], cv2.COLOR_RGB2GRAY),  # 转换为灰度图
            cv2.cvtColor(temp_list[temp_count - 1], cv2.COLOR_RGB2GRAY),
            buildImageSettings.compare_method,
        )  # 指定算法
        captureData.add_diff(  # 保存到数据类
            image1=f"capture{total_count - 1}{captureSettings.save_format}",
            image2=f"capture{total_count}{captureSettings.save_format}",
            compare_method=buildImageSettings.compare_method,
            diff=diff,
        )
        # 与阈值相比较
        if buildImageSettings.compare_method == "SSIM":
            is_different = diff < buildImageSettings.compare_threshold
        elif buildImageSettings.compare_method == "MSE":
            is_different = diff > buildImageSettings.compare_threshold
        else:
            log.error("未知算法类型")
            return
        # 输出diff至log
        if is_different:
            log.info(
                f"{buildImageSettings.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}"
            )
        else:
            log.debug(
                f"{buildImageSettings.compare_method}-{str(total_count - 1)}-{str(total_count)}={str(round(diff, 5))}"
            )

        # 保存去重后的图像
        if is_different or (
            stop_flag and captureSettings.if_keep_last
        ):  # 对最后一组进行保留
            if len(temp_list) > 2:  # 只保留缓存图像为三张以上的情况，以消除抖动
                # 对temp图像取平均值，不计首尾两张，计算时转换格式为uint16，以避免求和数据溢出
                image: np.ndarray = np.astype(
                    np.average(
                        [np.array(i, dtype=np.uint16) for i in temp_list[1:-1]],
                        axis=0,
                    ),  # 延0轴求和，保留图片数组形状
                    np.uint8,
                )  # 转换回uint8格式
                image_list.append(image)
                image_count += 1
                save_filename = f"image{image_count}{captureSettings.save_format}"
                save_image(working_dir / save_filename, image)
                if signalBuildImage:
                    signalBuildImage.emit(working_dir / save_filename)
                log.success(
                    f"output image{image_count} from "
                    f"capture{total_count - temp_count + 1}-{total_count - 1}"
                )
            temp_list.clear()  # 清除缓存
            temp_count = -1  # 重置计数
        if stop_flag:  # 检测信号跳出循环
            stop_flag.set(False)
            log.success("===本次截图完成===")
            captureData.save_to_file(
                working_dir / captureSettings.capture_data_filename
            )
            return
        time.sleep(captureSettings.delay_time)  # 延时


class CaptureThread(BaseTaskThread):
    signalBuildImage: Signal = Signal(Path)

    def __init__(
        self,
        captureSettings: CaptureSettings,
        buildImageSettings: BuildImageSettings,
        region_data: RegionData,
        working_dir: Directory,
    ) -> None:
        super().__init__()
        self.captureSettings: CaptureSettings = captureSettings
        self.buildImageSettings: BuildImageSettings = buildImageSettings
        self.regionData: RegionData = region_data
        self.working_dir = working_dir
        self.stop_flag: Flag = Flag(False)  # 中止线程信号

    def main(self, logger) -> None:
        """截图主函数"""
        start_capture_loop(
            captureSettings=self.captureSettings.model_copy(deep=True),
            buildImageSettings=self.buildImageSettings.model_copy(deep=True),
            regionData=self.regionData.model_copy(deep=True),
            working_dir=self.working_dir,
            stop_flag=self.stop_flag,
            logger=logger,
            signalBuildImage=self.signalBuildImage,
        )
