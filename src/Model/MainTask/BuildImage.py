import os

import cv2
import numpy as np
from pydantic import validate_call
from PySide6.QtWidgets import QApplication

from src.Model.Data.data import CaptureData
from src.Model.Data.settings import BuildImageSettings, CaptureSettings
from src.Model.Data.type import DirectoryExisting
from src.Model.image_process import compare_image, invert_image
from src.Model.MainTask.BaseTaskThread import BaseTaskThread
from src.Model.utils import get_numbered_image_names, read_image, save_image


@validate_call
def build_images(
    buildImageSettings: BuildImageSettings,
    captureSettings: CaptureSettings,
    working_dir: DirectoryExisting,
    logger=None,
) -> None:
    if not logger:
        from loguru import logger as log
    else:
        log = logger
    os.chdir(working_dir)
    log.debug(f"Working dir: {working_dir}")

    # 获取capture图像文件名列表
    file_names = get_numbered_image_names(working_dir, "capture")
    if file_names == []:
        return

    # 清除旧的image文件
    image_files = get_numbered_image_names(working_dir, "image")
    for f in image_files:
        os.remove(working_dir / f)

    # 获取差异值信息
    if "CaptureData.json" in os.listdir(working_dir):
        captureData = CaptureData.load_from_file(working_dir / "CaptureData.json")
    else:
        captureData = CaptureData()
    diff_list: list[float] = []
    captures = [read_image(working_dir / f) for f in file_names]
    for n in range(len(captures) - 1):
        diff = captureData.get_diff(
            file_names[n], file_names[n + 1], buildImageSettings.compare_method
        )
        if not diff:
            diff = compare_image(
                cv2.cvtColor(captures[n], cv2.COLOR_RGB2GRAY),
                cv2.cvtColor(captures[n + 1], cv2.COLOR_RGB2GRAY),
                method=buildImageSettings.compare_method,
            )
            log.debug(
                f"{buildImageSettings.compare_method}-{file_names[n]}:{file_names[n + 1]}-{diff}"
            )
            captureData.add_diff(
                file_names[n],
                file_names[n + 1],
                buildImageSettings.compare_method,
                diff,
            )
        diff_list.append(diff)
    captureData.save_to_file(working_dir / "CaptureData.json")

    # 对图像取平均
    image_count = 0
    if buildImageSettings.compare_method == "SSIM":
        different_index = [
            n + 1
            for n in range(len(diff_list))
            if diff_list[n] < buildImageSettings.compare_threshold
        ]
    elif buildImageSettings.compare_method == "MSE":
        different_index = [
            n + 1
            for n in range(len(diff_list))
            if diff_list[n] > buildImageSettings.compare_threshold
        ]
    else:
        log.error(
            QApplication.translate("BuildImages", "Invalid compare method {}").format(
                buildImageSettings.compare_method
            )
        )
        return
    different_index.append(0)
    if captureSettings.if_keep_last:
        different_index.append(len(diff_list) + 1)  # 添加最后一组
    different_index = list(set(different_index))  # 先去重
    different_index.sort()  # 后排序
    image_names_couple = [
        (file_names[different_index[n] + 1], file_names[different_index[n + 1] - 2])
        for n in range(len(different_index) - 1)
    ]
    log.debug(f"{image_names_couple=}")
    capture_sequnce = [
        captures[different_index[n] : different_index[n + 1]]
        for n in range(len(different_index) - 1)
    ]
    capture_sequnce = [i for i in capture_sequnce if len(i) > 2]
    image_count = 0
    for sequnce in capture_sequnce:
        image = np.average(
            [
                np.asarray(i).astype(np.uint16)  # 转换为uint16，避免求和数据溢出
                for i in sequnce[1:-1]
            ],  # 不要首尾两张
            axis=0,  # 保留图片形状
        ).astype(np.uint8)  # 转换回图片格式
        if captureSettings.if_invert_image:
            image = invert_image(image)
        save_image(
            working_dir / f"image{image_count}{captureSettings.save_format}", image
        )
        image_count += 1
    log.success(QApplication.translate("BuildImage", "Image build completed."))


class BuildImageThread(BaseTaskThread):
    def __init__(
        self,
        buildImageSettings: BuildImageSettings,
        captureSettings: CaptureSettings,
        working_dir: DirectoryExisting,
    ) -> None:
        super().__init__()
        self.buildImageSettings: BuildImageSettings = buildImageSettings
        self.captureSettings: CaptureSettings = captureSettings
        self.working_dir: DirectoryExisting = working_dir

    def main(self, logger) -> None:
        build_images(
            buildImageSettings=self.buildImageSettings.model_copy(deep=True),
            captureSettings=self.captureSettings.model_copy(deep=True),
            working_dir=self.working_dir,
            logger=logger,
        )
