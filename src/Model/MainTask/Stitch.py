import os

import cv2
import numpy as np
from fast_ssim import ssim
from pydantic import PositiveInt, validate_call

from src.Model.Data.const import StitchMethod
from src.Model.Data.data import ImageData, ScoreDetections, ScoreStitchData
from src.Model.Data.settings import (
    Direction,
    LineDetectorSettings,
    StitchSettings,
)
from src.Model.Data.type import DirectoryExisting, GrayImageArray
from src.Model.image_process import (
    clip_image,
    detect_horizontal_lines,
    detect_vertical_lines,
    get_barline_num_region,
    stitch_images,
)
from src.Model.MainTask.BaseTaskThread import BaseTaskThread
from src.Model.utils import (
    get_numbered_image_names,
    read_image,
    read_numbered_images,
    save_image,
)


@validate_call
def stitch_image_task(
    stitchSettings: StitchSettings,
    detectorSettings: LineDetectorSettings,
    working_dir: DirectoryExisting,
    logger=None,
) -> None:
    if not logger:
        from loguru import logger as log
    else:
        log = logger
    os.chdir(working_dir)
    log.debug(f"Working dir: {working_dir}")

    score_title: str = working_dir.name
    scoreDetections = ScoreDetections(directory=working_dir)
    image_filenames: list[str] = []

    if (f := (working_dir / "ScoreDetections.json")).exists():
        try:
            scoreDetections: ScoreDetections = ScoreDetections.load_from_file(f)
            image_filenames = scoreDetections.get_image_filenames()
            log.debug("成功读取缓存，跳过线段检测")
        except Exception:
            log.warning(f"ScoreDetections load failed: {f}")
    if (
        stitchSettings.method != "DIRECT"
        and scoreDetections.get_image_filenames() == []  # load failed
    ):
        # 获取检测数据
        log.info("开始检测图像中的线段")
        for f in working_dir.glob("*image*-detected.*"):
            os.remove(f)
        for f in working_dir.glob("*image*"):
            image_filenames.append(f.name)
            image = read_image(f)
            image_gray = np.asarray(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
            horizontal_lines = detect_horizontal_lines(
                image_gray, detectorSettings.coefficient_horizontal
            )
            vertical_lines = detect_vertical_lines(
                image_gray, horizontal_lines, detectorSettings.coefficient_vertical
            )
            for line in horizontal_lines + vertical_lines:
                line.draw(image)
            saving_filename = (
                f.name.split(".")[0] + "-detected" + stitchSettings.saving_format
            )
            save_image(working_dir / saving_filename, image)
            scoreDetections.add_image(
                ImageData(filename=f.name, image=image),
                horizontal_lines,
                vertical_lines,
            )
            log.debug(
                f"{f.name}-horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}"
            )
        scoreDetections.save_to_file(working_dir / "ScoreDetections.json")
        log.info("线段检测完毕，已生成对应预览图")
    else:
        image_filenames = [f.name for f in working_dir.glob("*image*")]
    if len(image_filenames) < 2:
        log.error("未发2现张或以上可供拼接的图像，请检查文件夹中image数目")
        return

    # 获取排序后的图片名称
    image_names = get_numbered_image_names(working_dir, "image")
    images = read_numbered_images(working_dir, "image", image_names)
    images_gray: list[GrayImageArray] = [
        cv2.cvtColor(i, cv2.COLOR_RGB2GRAY) for i in images
    ]

    log.debug("Stitch method: " + stitchSettings.method)
    log.debug("Stitch direction: " + stitchSettings.direction.str)
    # 获取mse最低时的拼接像素点
    if stitchSettings.method == "DIRECT":
        log.info("直接拼接模式，跳过比对")
        stitch_points = [0] * (len(images) - 1)
    else:
        log.info("比对图片中")
        stitch_points: list[int] = []
        stitch_direction = stitchSettings.direction
        # 拼接参考线方向，与拼接方向相反
        ref_line_direction: Direction = stitch_direction.reverse
        for name_index in range(len(image_names) - 1):
            img1: GrayImageArray = images_gray[name_index]
            img2: GrayImageArray = images_gray[name_index + 1]
            length = img1.shape[stitch_direction]  # 拼接方向上的长度
            stitch_index = get_stitch_index(
                image_names[name_index],
                image_names[name_index + 1],
                length,
                scoreDetections,
                ref_line_direction,
                log,
            )
            stitch_points.append(
                get_stitch_point(
                    img1,
                    img2,
                    stitch_index,
                    stitch_direction,
                    stitchSettings.method,
                    scoreDetections,
                )
            )

            log.debug(
                f"{stitch_direction.str}:{stitchSettings.method}-"
                f"{image_names[name_index]}-{image_names[name_index + 1]}"
                f"-stitch_point:{stitch_points[-1]}"
            )
        log.info("图像比对完毕")

    # 保存拼接点数据
    scoreStitchData = ScoreStitchData(stitch_settings=stitchSettings)
    scoreStitchData.add_points(stitch_points, images, image_names)
    scoreStitchData.save_to_file(working_dir / "ScoreStitchData.json")

    # 进行拼接
    log.info("图像拼接中")
    final_image = stitch_images(images, stitch_points, stitchSettings.direction)
    saving_filename = score_title + "-stitched" + stitchSettings.saving_format
    save_image(working_dir / saving_filename, final_image)
    log.info(f"图像拼接完毕，已生成预览图{working_dir / saving_filename}")


@validate_call
def get_stitch_index(
    name_img1: str,
    name_img2: str,
    stitch_length: PositiveInt,
    scoreDetections: ScoreDetections,
    ref_line_direction: Direction,
    log=None,
) -> list[int]:
    """Get stitch index area for compare computing"""
    try:
        line_index = scoreDetections[name_img1].get_lines_index(
            reverse=True, extern_width=2, direction=ref_line_direction
        )
        stitch_indexs = [
            line_index + line.start_index
            for line in scoreDetections[name_img2].get_lines(
                direction=ref_line_direction
            )
        ]
        stitch_indexs = np.unique(
            np.concatenate(stitch_indexs)
        )  # 拼接成一维数组并进行去重
        stitch_index: list[int] = list(
            stitch_indexs[stitch_indexs < stitch_length]
        )  # 限定拼接索引区域范围
    except ValueError:
        stitch_index = []
    if stitch_index == []:  # 当img1，img2无重合特征线时
        log.warning(
            f"{name_img1}与{name_img2}无重合特征线，将在中间区域进行比对"
        ) if log else None
        stitch_index = [  # 取中间3/5的区域
            i for i in range(int(stitch_length * 0.2), int(stitch_length * 0.8))
        ]  # stitch_index不能为0!!!

    return stitch_index


@validate_call
def get_stitch_point(
    img1: GrayImageArray,
    img2: GrayImageArray,
    stitch_index: list[PositiveInt],
    direction: Direction,
    method: StitchMethod,
    scoreDetections: ScoreDetections,
    log=None,
):
    if method == StitchMethod.SSIM:
        # SSIM算法要求最小图像大小
        stitch_index = [offset for offset in stitch_index if offset > 7]
        diff = np.empty_like(stitch_index, dtype=np.float32)
        # 在水平模式中，增加小节数字序号区域的权重
        if direction == Direction.HORIZONTAL:
            # 获取小节数字序号的区域，以设置权重
            barline_num_detect_start, barline_num_detect_end = get_barline_num_region(
                scoreDetections[0]
            )
            ex_diff = diff.copy()

        for i, offset in enumerate(stitch_index):
            diff[i] = ssim(
                clip_image(img1, direction, (-offset, None)),
                clip_image(img2, direction, (None, offset)),
                data_range=255,
            )
            if direction == Direction.HORIZONTAL:
                ex_diff[i] = ssim(
                    img1[
                        barline_num_detect_start:barline_num_detect_end,
                        -offset:,
                    ],
                    img2[barline_num_detect_start:barline_num_detect_end, :offset],
                    data_range=255,
                )

        if direction == Direction.HORIZONTAL:
            diff = diff * 0.2 + ex_diff * 0.8
        # 右侧1像素为img2的部分，越大越相似
        return int(stitch_index[np.argmax(diff)] + 1)
    elif method == StitchMethod.MSE:
        diff = np.empty_like(stitch_index)
        for i, offset in enumerate(stitch_index):
            diff[i] = np.std(  # ！！！避免差值数据溢出
                clip_image(img1, direction, (-offset, None)).astype(np.uint16)
                - clip_image(img2, direction, (None, offset)).astype(np.uint16)
            )
        # 同上，diff越小越相似
        return int(stitch_index[np.argmin(diff)] + 1)


class StitchThread(BaseTaskThread):
    def __init__(
        self,
        stitchSettings: StitchSettings,
        detectorSettings: LineDetectorSettings,
        working_dir: DirectoryExisting,
    ):
        super().__init__()
        self.stitchSettings: StitchSettings = stitchSettings
        self.detectorSettings: LineDetectorSettings = detectorSettings
        self.working_dir = working_dir

    def main(self, logger) -> None:
        stitch_image_task(
            stitchSettings=self.stitchSettings.model_copy(deep=True),
            detectorSettings=self.detectorSettings.model_copy(deep=True),
            working_dir=self.working_dir,
            logger=logger,
        )
