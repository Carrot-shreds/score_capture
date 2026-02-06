import os
from copy import deepcopy
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import FreeTypeFont
from pydantic import validate_call

from src.Model.Data.const import Align, Direction, ReclipMethod
from src.Model.Data.data import ReclipData, ScoreDetections, StyleData
from src.Model.Data.settings import LineDetectorSettings, ReclipSettings
from src.Model.Data.type import DirectoryExisting, FilePath, ImageArray, Line
from src.Model.image_process import (
    clip_image,
    detect_all_lines_with_clip,
    detect_horizontal_lines,
)
from src.Model.MainTask.BaseTaskThread import BaseTaskThread
from src.Model.utils import read_image, save_image


@validate_call
def reclip_image(
    detectorSettings: LineDetectorSettings,
    reclipSettings: ReclipSettings,
    working_dir: DirectoryExisting,
    font_path: FilePath,
    logger=None,
    style_data: StyleData | None = None,
) -> None:
    if not logger:
        from loguru import logger as log
    else:
        log = logger
    os.chdir(working_dir)
    log.debug(f"Working dir: {working_dir}")

    if style_data:
        pass
    elif "StyleData.json" in working_dir.iterdir():
        style_data = StyleData.load_from_file(working_dir / "StyleData.json")
    else:
        style_data = StyleData()
        style_data.save_to_file(working_dir / "StyleData.json")

    score_title = working_dir.name
    try:
        stitched_image_filename = working_dir.glob(
            f"{score_title}-stitched.*"
        ).__next__()
    except StopIteration:
        log.error(
            f"未在当前工作目录下发现'{score_title}-stitched.*'图片，请先进行拼接操作"
        )
        return
    stitched_image_path = working_dir / stitched_image_filename
    stitched_detected_image_filename = (
        f"{score_title}-stitched-detected.{reclipSettings.saving_format}"
    )
    if (working_dir / stitched_detected_image_filename).exists():
        os.remove(working_dir / stitched_detected_image_filename)

    stitched_image = read_image(stitched_image_path)
    stitched_image_gray = cv2.cvtColor(stitched_image, cv2.COLOR_RGB2GRAY)
    if stitched_image.shape[0] > stitched_image.shape[1]:
        # vertical stitched
        reclip_data = ReclipData(
            clip_direction=Direction.HORIZONTAL,
            clip_indexes=[],
            clip_height=0,
        )
        reclip_save_filename = score_title + "-reclip" + reclipSettings.saving_format
        reclip_data.save_to_file(working_dir / "ReclipData.json")
        save_image(working_dir / reclip_save_filename, stitched_image)

        blank_line_index = get_gap_line_index(
            stitched_image, detectorSettings, working_dir
        )

        style_restitched_clips(
            log,
            working_dir,
            reclipSettings,
            stitched_image,
            style_data,
            blank_line_index,
            font_path,
        )
        return

    # 获取检测数据
    log.info("开始检测图像中的线段")
    if "ScoreDetections.json" in os.listdir(working_dir):
        clip_length = ScoreDetections.load_from_file(
            working_dir / "ScoreDetections.json"
        )[0].image_shape[1]
    else:
        clip_length = 800
    horizontal_lines, vertical_lines = detect_all_lines_with_clip(
        stitched_image_gray,
        clip_length,
        detectorSettings.coefficient_horizontal,
        detectorSettings.coefficient_vertical,
    )
    stitched_detected_image = deepcopy(stitched_image)
    for line in horizontal_lines + vertical_lines:
        line.draw(stitched_detected_image)
    save_image(working_dir / stitched_detected_image_filename, stitched_detected_image)
    log.debug(f"horizontal:{len(horizontal_lines)}-vertical:{len(vertical_lines)}")
    log.info("线段检测完毕，已生成对应预览图")

    # 小节线分组
    index = np.asarray([line.start_index for line in vertical_lines])
    distance: np.ndarray = index[1:] - index[:-1]
    del_index: list[int] = []
    for i in np.where(distance < np.average(distance) / 5)[0]:
        vertical_lines[i].thickness = (
            vertical_lines[i + 1].end_index - vertical_lines[i].start_index
        )
        del_index.append(i + 1)
    bar_lines: list[Line] = list(np.delete(np.asarray(vertical_lines), del_index))
    detected_barlines_image = deepcopy(stitched_image)
    for line in bar_lines:
        line.draw(detected_barlines_image)
    detected_barlines_filename = (
        score_title + "-detected-barlines" + reclipSettings.saving_format
    )
    save_image(working_dir / detected_barlines_filename, detected_barlines_image)
    log.info(f"成功对小节线进行归类，共检测出{len(bar_lines)}组小节线,预览图像已保存")

    # 进行切片
    log.debug("开始进行切片操作")
    image_clips: list[np.ndarray] = []
    clip_index: list[tuple[int, int]] = []
    extern_pixel = reclipSettings.clip_margin  # 切片左右额外包含的像素
    if reclipSettings.method == ReclipMethod.FIXED_BAR_NUM:  # 每行固定小节数
        each_line_bar_num = reclipSettings.bar_num_each_line  # 每行的固定小节数
        for i in range(len(bar_lines)):
            if (
                len(bar_lines) - i <= each_line_bar_num
            ):  # 包含最后一组余数，随后跳出循环
                clip_index.append(
                    (
                        bar_lines[i].start_index - extern_pixel,
                        bar_lines[-1].end_index + extern_pixel,
                    )
                )
                break
            elif i % each_line_bar_num == 0:
                clip_index.append(
                    (
                        bar_lines[i].start_index - extern_pixel,
                        bar_lines[i + each_line_bar_num].end_index + extern_pixel,
                    )
                )
                if i == len(bar_lines) - 1 - each_line_bar_num:
                    break
    elif reclipSettings.method == ReclipMethod.FILL_MAX_WIDTH:  # 填充每行最大长度
        bar_lines_index = np.asarray([i.start_index for i in bar_lines])
        max_length = (
            bar_lines[reclipSettings.bar_num_line_max_length].end_index
            - bar_lines[0].start_index
        )  # 使用前n小节的总长度作为限制长度
        result_index = [bar_lines_index[0]]
        for i in range(bar_lines_index.size):
            if bar_lines_index[i] - result_index[-1] >= max_length:
                # 取i-1,不超过最大长度的部分
                result_index.append(bar_lines_index[i - 1])
        result_index = np.concatenate(  # 图片索引转lines索引
            [np.where(bar_lines_index == i)[0] for i in result_index]
        )
        if result_index[-1] != bar_lines_index.size - 1:
            result_index = np.append(
                result_index, bar_lines_index.size - 1
            )  # 添加入最后一组
        clip_index = [
            (
                bar_lines[result_index[i]].start_index - extern_pixel,
                bar_lines[result_index[i + 1]].end_index + extern_pixel,
            )
            for i in range(result_index.size - 1)
        ]
    for i in clip_index:
        clip_start = max(0, i[0])  # 确保起始位置不小于0
        clip_end = min(stitched_image.shape[1], i[1])  # 确保结束位置不大于图片宽度
        image_clips.append(stitched_image[:, clip_start:clip_end, :])  # 切片
    log.debug("成功完成切片操作")

    reclip_data = ReclipData(
        clip_direction=Direction.VERTICAL,
        clip_indexes=clip_index,
        clip_height=image_clips[0].shape[0],
    )
    reclip_data.save_to_file(working_dir / "ReclipData.json")

    # 拼接
    log.debug("开始进行拼接操作")
    canvas: np.ndarray = (
        np.ones_like(image_clips[np.argmax([c.size for c in image_clips])]).astype(
            np.uint8
        )
        * 255
    )  # 白色画布
    canvas = np.concatenate(
        [canvas for _ in range(len(image_clips))], axis=0
    )  # 将画布的高度拓展len(clips)倍
    current_y: int = 0
    canvas_width: int = canvas.shape[1]
    for c in image_clips:
        c: np.ndarray
        if (
            reclipSettings.clip_resize
            and c.shape[1] != canvas_width
            and reclipSettings.clip_resize_threshold < c.shape[1] / canvas_width
        ):
            c = cv2.resize(
                c, (canvas_width, c.shape[0]), interpolation=cv2.INTER_CUBIC
            )  # 图像缩放插值方法
        h = c.shape[0]
        w = c.shape[1]
        if reclipSettings.clip_align == Align.LEFT:  # 靠左
            canvas[current_y : current_y + h, 0:w, :] = c
        elif reclipSettings.clip_align == Align.CENTER:  # 居中
            space = int((canvas_width - w) / 2)
            canvas[current_y : current_y + h, space : w + space, :] = c
        elif reclipSettings.clip_align == Align.RIGHT:  # 靠右
            canvas[current_y : current_y + h, canvas_width - w : canvas_width, :] = c
        current_y += h
    reclip_save_filename = score_title + "-reclip" + reclipSettings.saving_format
    save_image(working_dir / reclip_save_filename, canvas)
    log.success(f"已重新切片拼接，保存图片到{working_dir / reclip_save_filename}")

    style_restitched_clips(
        log,
        working_dir,
        reclipSettings,
        canvas,
        style_data,
        image_clips[0].shape[0],
        font_path,
    )


def get_gap_line_index(
    stitched_image: ImageArray,
    detector_settings: LineDetectorSettings,
    working_dir: Path,
) -> list[int]:
    """get white gaps between sheet rows"""
    blank_gaps = detect_horizontal_lines(
        cv2.cvtColor(stitched_image, cv2.COLOR_RGB2GRAY),
        coefficient=detector_settings.coefficient_horizontal,
        reverse=True,
        r_pixel_threshold=detector_settings.h_reverse_pixel_threshold,
        r_thickness_threshold=detector_settings.h_reverse_thickness_threshold,
    )
    draw = deepcopy(stitched_image)
    for line in blank_gaps:
        line.draw(draw)
    blank_line_index = [  # use central index of a line
        int(np.average([line.start_index, line.end_index])) for line in blank_gaps
    ]
    if blank_line_index == []:
        raise ValueError(
            "Empty lines of sheet gaps! Please try to turn down your reverse horizontal line thresholds"
        )
    save_image(working_dir / f"{working_dir.name}-blank-gaps.jpg", draw)
    return blank_line_index


@validate_call
def style_restitched_clips(
    log,
    working_dir: DirectoryExisting,
    reclip_settings: ReclipSettings,
    restitched_image: ImageArray,
    style_data: StyleData,
    clip_height: list[int] | int,
    font_path: FilePath,
):
    log.debug("Editing score style")
    score_width = restitched_image.shape[1]
    canvas_width = int(score_width / (1 - style_data.margin_width))  # with margin
    canvas_height = int(canvas_width * 1.414)  # A4 shape
    canvas_margin_width = int((canvas_width - score_width) / 2)
    canvas_margin_height = int((canvas_height * style_data.margin_height) / 2)
    canvas_margin_title = int(canvas_height * style_data.margin_title)
    score_cut_height_with_title = (
        canvas_height - canvas_margin_width - canvas_margin_title
    )
    score_cut_height = canvas_height - canvas_margin_height * 2
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255
    stitched_image_length = restitched_image.shape[0]

    cut_indexes: list[int] = [0]
    cut_clip_num: int = 1
    while True:
        if isinstance(clip_height, int):
            height = clip_height * cut_clip_num
        else:
            if cut_clip_num - 1 == len(clip_height):
                if cut_indexes[-1] < stitched_image_length:
                    cut_indexes.append(stitched_image_length)
                break
            height = clip_height[cut_clip_num - 1] - cut_indexes[-1]

        if height < (
            score_cut_height_with_title
            if len(cut_indexes) == 1 and style_data.add_title
            else score_cut_height
        ):
            cut_clip_num += 1
            continue

        if isinstance(clip_height, int):
            cut_indexes.append(cut_indexes[-1] + height - clip_height)
            cut_clip_num = 1
            if cut_indexes[-1] > restitched_image.shape[0]:
                cut_indexes[-1] = restitched_image.shape[0]
                break
        else:
            cut_indexes.append(clip_height[cut_clip_num - 1 - 1])
    log.debug(f"{cut_indexes=}")
    log.debug(
        f"cut_page_heights={[cut_indexes[i + 1] - cut_indexes[i] for i in range(len(cut_indexes) - 1)]}"
    )
    score_pages: list[ImageArray] = [
        clip_image(
            restitched_image, Direction.VERTICAL, (cut_indexes[i], cut_indexes[i + 1])
        )
        for i in range(len(cut_indexes) - 1)
    ]

    if old_images := list(working_dir.glob(f"{working_dir.name}*[0-9]*")):
        [os.remove(i) for i in old_images]

    page_num_height = int(canvas_margin_height * 0.5)
    page_num_height = (
        page_num_height if page_num_height > (m := int(canvas_height / 50)) else m
    )
    page_num_width = int(page_num_height * 1.5)
    page_num_font = (
        get_auto_sized_font(
            str(99),
            font_path,
            page_num_width,
            page_num_height,
            ImageDraw(Image.new("RGB", (0, 0))),
            10,
        )
        if style_data.add_page_num
        else None
    )
    page_num_xy = (
        int(canvas_width - page_num_width / 2),
        int(canvas_height - page_num_height * 1.5),
    )
    for i, s in enumerate(score_pages):
        if i == 0 and style_data.add_title:
            start_y = canvas_margin_title
        else:
            start_y = canvas_margin_height
        c = deepcopy(canvas)
        try:
            c[
                start_y : start_y + s.shape[0],
                canvas_margin_width : canvas_margin_width + s.shape[1],
                :,
            ] = s
        except ValueError as e:
            log.warning(e)
            log.warning(
                f"{working_dir.name}{i}{reclip_settings.saving_format} clip failed."
                "This may caused by too large cut height that out off the page bound."
                "Check your height between cut_indexes, and try turning down your threshold reverse horizontal"
            )
            return

        pil_image = Image.fromarray(c)
        draw = ImageDraw(pil_image)
        if i == 0 and style_data.title != "" and style_data.add_title:  # draw title
            title_w = int(score_width * 0.8)
            title_h = int(canvas_margin_title * 0.5)
            title_font = get_auto_sized_font(
                style_data.title, font_path, title_w, title_h, draw, 100
            )
            title_xy = (int(canvas_width / 2), int(canvas_margin_title / 2))
            draw.text(
                xy=title_xy,
                text=style_data.title,
                font=title_font,
                fill=(0, 0, 0),
                anchor="mm",
            )

        draw.text(
            xy=page_num_xy,
            text=str(i + 1),
            font=page_num_font,
            fill=(0, 0, 0),
            anchor="mm",
        ) if page_num_font else None

        filename = f"{working_dir.name}{i}{reclip_settings.saving_format}"
        pil_image.save(working_dir / filename)
        log.info(f"Save final image to: {working_dir / filename}")


def get_auto_sized_font(
    text: str,
    font_path: Path,
    max_width: int,
    max_height: int,
    image_draw: ImageDraw,
    step: int = 100,
) -> FreeTypeFont:
    font_size = step
    while True:
        title_font = ImageFont.truetype(font=font_path, size=font_size)
        left, top, right, bottom = image_draw.textbbox(
            xy=(0, 0),
            text=text,
            font=title_font,
        )
        if abs(right - left) > max_width or abs(top - bottom) > max_height:
            break
        font_size += step
    return ImageFont.truetype(
        font=font_path, size=(font_size - step) if font_size > step else step
    )


class ReclipThread(BaseTaskThread):
    def __init__(
        self,
        reclipSettings: ReclipSettings,
        detectorSettings: LineDetectorSettings,
        working_dir: DirectoryExisting,
        font_path: FilePath,
        style_data: StyleData | None = None,
    ):
        super().__init__()
        self.reclipSettings: ReclipSettings = reclipSettings
        self.detectorSettings: LineDetectorSettings = detectorSettings
        self.working_dir: DirectoryExisting = working_dir
        self.font_path = font_path
        self.style_data = style_data

    def main(self, logger) -> None:
        reclip_image(
            detectorSettings=self.detectorSettings.model_copy(deep=True),
            reclipSettings=self.reclipSettings.model_copy(deep=True),
            working_dir=self.working_dir,
            font_path=self.font_path,
            logger=logger,
            style_data=self.style_data,
        )
