import cv2
import numpy as np
from fast_ssim import ssim
from loguru import logger as log
from PIL.Image import Image
from pydantic import validate_call
from PySide6.QtWidgets import QApplication

from src.Model.Data.const import Direction, ImageCompareMethod
from src.Model.Data.data import ImageDetection
from src.Model.Data.type import GrayImageArray, ImageArray, Line


def gama_transfer(img, threshold, power) -> ImageArray:
    """对灰度图应用伽马转换，对灰度值除于阈值后进行幂运算，并线性映射到0-255范围"""
    img = np.power(img / threshold, power) * (
        np.power(255 / threshold, power) * threshold / 255
    )
    return np.asarray(np.round(img), np.uint8)


@validate_call
def detect_horizontal_lines(
    img: ImageArray,
    coefficient: float = 0.7,
    invert: bool = False,
    r_pixel_threshold: float = 255,
    r_thickness_threshold: int = 10,
) -> list[Line]:
    """img为灰度图(二维数组)，识别并返回所有水平线段(白色背景图中的黑色线)"""
    if len(img.shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    if np.average(img) < 128:
        img = 255 - img  # 将图像反相为白底图

    img_adaptive: np.ndarray = (
        cv2.adaptiveThreshold(  # 图像预处理，自适应二值化，需输入白底图像
            img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 7
        )
    )
    average_row: np.ndarray = np.average(img_adaptive, axis=1)
    if not invert:
        result_index: list[int] = [
            i for i in range(len(average_row)) if average_row[i] < 255 * coefficient
        ]
    else:
        result_index: list[int] = [
            i for i in range(len(average_row)) if average_row[i] >= r_pixel_threshold
        ]

    lines: list[Line] = []
    current_y: int = 1  # result比img短2个单位，等效于从img的1像素开始
    point_y: int = 0
    thickness: int
    for i in range(len(average_row)):
        if i in result_index and (not point_y):  # 平均值低于阈值时
            point_y = current_y
        elif i not in result_index and point_y:
            thickness = current_y - point_y  # 计算线段厚度
            lines.append(
                Line(
                    point1=(0, point_y),
                    point2=(len(img[0]) - 1, point_y),
                    thickness=thickness,
                    direction=Direction.HORIZONTAL,
                    image_shape=img.shape,
                )
            )
            point_y = 0
        current_y += 1
    if invert:
        lines = [line for line in lines if line.thickness >= r_thickness_threshold]

    if not lines:
        log.warning(
            QApplication.translate("detect_horizontal_lines", "Empty horizontal line.")
        )
    return lines


@validate_call
def get_score_lines(horizontal_lines: list[Line]) -> list[Line]:
    """从水平线检测结果中获取曲谱部分的横线"""
    # TODO 使用聚类算法改写~
    if len(horizontal_lines) < 3:
        return []

    horizontal_lines_ys = np.asarray([line.point1[1] for line in horizontal_lines])
    distance = horizontal_lines_ys[1:] - horizontal_lines_ys[:-1]
    index = (
        np.argwhere(
            (distance - np.average(distance, axis=0)) / (np.std(distance) + 0.1) > 2
        )
        + 1
    )
    index = np.sort(np.append(index, [0, len(horizontal_lines)]))
    index = [(int(index[i]), int(index[i + 1])) for i in range(np.shape(index)[0] - 1)]
    index = [i for i in index if (i[1] - i[0]) > 3]

    try:
        result = [horizontal_lines[i:j] for i, j in index][-1]
    except IndexError:
        log.debug("Get no staff lines from horizontal lines.")
        return []
    return result


# pyright: reportRedeclaration=false
@validate_call
def detect_vertical_lines(
    image: ImageArray,
    horizontal_lines_data: list[Line] | None,
    coefficient: float = 0.9,
) -> list[Line]:
    """img为灰度图(二维数组)，识别并返回所有竖直线段(黑色背景图中的白色线)"""
    # TODO 异常处理
    img = _image_preprocess_for_vertical_line_detect(image)

    # Check horizontal lines
    if horizontal_lines_data is None:
        horizontal_lines: list[Line] = detect_horizontal_lines(img)
    else:
        horizontal_lines: list[Line] = horizontal_lines_data
    if not horizontal_lines:
        log.info(
            QApplication.translate(
                "detect_vertical_lines",
                "Skip vertical line detect, due to empty horizontal line.",
            )
        )
        return []
    horizontal_lines = get_score_lines(horizontal_lines)  # 水平线预处理
    if not horizontal_lines:
        log.info(
            QApplication.translate(
                "detect_vertical_lines",
                "Skip vertical line detect, due to empty staff line.",
            )
        )
        return []

    # 识别区域
    top_line_y: int = horizontal_lines[0].start_index  # 线谱中最上方的那条线
    bottom_line_y: int = horizontal_lines[-1].end_index  # 最下方的那条线
    expand: int = int((bottom_line_y - top_line_y) / 5)
    edge_top: int = top_line_y - expand  # 上方延伸区域
    edge_bottom: int = bottom_line_y + expand  # 下方延伸区域
    edge_top = edge_top if edge_top > 0 else 0  # 限制上边界
    edge_bottom = (
        edge_bottom if edge_bottom < (h := img.shape[0]) else h - 1
    )  # 限制下边界

    # 定义竖直方向的内核，用于连接二值化导致直线上产生的断点
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (2, int((bottom_line_y - top_line_y) / 15))
    )
    # 执行形态学闭运算，先膨胀后腐蚀，以连接断点
    img: np.ndarray = cv2.morphologyEx(img, cv2.MORPH_CLOSE, vertical_kernel)

    bar_lines_indexes_group: list[np.ndarray] = _detect_bar_lines(
        img, top_line_y, bottom_line_y, edge_top, edge_bottom, coefficient
    )

    try:
        result = [
            Line(
                point1=(line[0], top_line_y),
                point2=(line[0], bottom_line_y),
                thickness=len(line),
                direction=Direction.VERTICAL,
                image_shape=(img.shape[0:2]),
            )
            for line in bar_lines_indexes_group
        ]
    except IndexError:
        log.warning(
            QApplication.translate(
                "detect_vertical_lines", "Get no vertical line from staff region."
            )
        )
        return []
    return result


def _image_preprocess_for_vertical_line_detect(image: ImageArray) -> GrayImageArray:
    if len(image.shape) != 2:
        img: np.ndarray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    else:
        img: np.ndarray = image

    if np.average(img) > 128:  # 图像整体偏亮时
        img: np.ndarray = (
            cv2.adaptiveThreshold(  # 图像预处理，自适应二值化，需输入白底灰度图像
                img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 7
            )
        )
        img = 255 - img  # 将图像反相为黑底图
    else:  # 图像整体偏暗时
        img: np.ndarray = 255 - image  # 先反相为白底图
        img = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 7
        )
        img = 255 - img  # 再反相为黑底图

    return img


def _detect_bar_lines(
    img, top_line_y, bottom_line_y, edge_top, edge_bottom, coefficient
) -> list[np.ndarray]:
    """Need max_value==255 binary black background image"""
    # 初步识别
    sum_columns: np.ndarray = np.sum(
        img[top_line_y:bottom_line_y], axis=0
    )  # 线谱中的和
    sum_columns_ex: np.ndarray = np.sum(
        img[edge_top:edge_bottom], axis=0
    )  # 包含延申范围
    # 将小于中点的值置为0，以仅保留突出的数据影响
    columns_midpoint: int = (np.max(sum_columns) + np.min(sum_columns)) >> 1
    sum_columns[np.where(sum_columns < columns_midpoint)[0]] = 0
    columns_ex_midpoint: int = (np.max(sum_columns_ex) + np.min(sum_columns_ex)) >> 1
    sum_columns_ex[np.where(sum_columns_ex < columns_ex_midpoint)[0]] = 0
    # 确保竖直线段没有超出线谱范围
    bar_lines: np.ndarray = np.where(
        (
            sum_columns / sum_columns.shape[0]
            - sum_columns_ex / sum_columns_ex.shape[0] * coefficient
        )
        > 0
    )[0]

    # 去除方差过大(上下不对称)的线段
    std_y = np.std(img[top_line_y:bottom_line_y, bar_lines], axis=0)
    del_index: np.ndarray = np.where(std_y > 100)[0]  # 测试经验数值
    bar_lines: np.ndarray = np.delete(bar_lines, del_index)

    # 去除前景色(白色)占比过少的线段
    white_ratio_y: np.ndarray = (
        np.sum(img[top_line_y:bottom_line_y, bar_lines], axis=0)
        / 255  # white==255, get white pixel num
        / (bottom_line_y - top_line_y)  # divide by total pixel num
    )
    del_index: np.ndarray = np.where(white_ratio_y < 0.93)[0]  # 测试经验数值
    bar_lines: np.ndarray = np.delete(bar_lines, del_index)

    # 结构化存储结果
    split_index: np.ndarray = np.where((bar_lines[1:] - bar_lines[:-1]) != 1)[0] + 1
    split_index: np.ndarray = np.sort(np.append(split_index, [0, len(bar_lines)]))[1:-1]
    result: list[np.ndarray] = np.split(bar_lines, split_index)
    return result


@validate_call
def detect_all_lines_with_clip(
    img: ImageArray,
    clip_length: int,
    coefficient_horizontal: float,
    coefficient_vertical: float,
) -> tuple[list[Line], list[Line]]:
    """将图片以指定长度切片后，进行水平与竖直线段的检测"""
    if len(img.shape) != 2:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图

    lines = [[], []]
    region: list[int] = [0, clip_length]
    while region[1] < (img.shape[1] - clip_length):
        if region[1] >= img.shape[1] - clip_length * 2:
            clipped_image = img[
                :, region[0] : img.shape[1]
            ]  # 保证最后一组长度clip_length<length<clip_length*2
        else:
            clipped_image = img[:, region[0] : region[1]]

        horizontal_lines = detect_horizontal_lines(
            clipped_image, coefficient_horizontal
        )
        for line in horizontal_lines:
            line.move_right(region[0], img.shape)  # 将线段向右移动指定像素值
        try:
            vertical_lines = detect_vertical_lines(
                clipped_image, horizontal_lines, coefficient_vertical
            )
        except IndexError:
            vertical_lines = []
        for line in vertical_lines:
            line.move_right(region[0], img.shape)

        lines[0] += horizontal_lines
        lines[1] += vertical_lines
        region[0] += clip_length
        region[1] += clip_length

    return lines[0], lines[1]


@validate_call
def get_barline_num_region(image_detection: ImageDetection) -> tuple[int, int]:
    """获取图片上半区域中，小节数上下的区域，用以对该区域加权计算"""
    point1_y = image_detection.vertical_lines[0].point1[1]  # 小节线的上方点y
    point2_y = image_detection.vertical_lines[0].point2[1]
    detect_width = abs(point2_y - point1_y)
    detect_start = int(point1_y - detect_width / 2)
    detect_start = detect_start if detect_start >= 0 else 0  # 防止出现负数
    detect_end = int(point1_y + detect_width / 2)
    return detect_start, detect_end


def image_pre_process(img: np.ndarray | Image, if_invert_image: bool) -> ImageArray:
    """图像预处理"""
    img = np.array(img, np.uint8)
    if if_invert_image:
        img = 255 - img
    # img = super_resolution(img)
    return img


@validate_call
def clip_image(
    image: ImageArray,
    direction: Direction,
    index: tuple[int | None, int | None],
) -> ImageArray:
    """按指定方向和索引对图像进行切片, (1,None)表示[1:]]"""
    start, end = index

    try:
        if direction == Direction.HORIZONTAL:
            if len(image.shape) == 2:  # 灰度图
                return image[:, start:end]
            elif len(image.shape) == 3:  # 彩色图
                return image[:, start:end, :]
            else:
                raise ValueError("Invalid image dimension, should be 2 or 3.")
        if direction == Direction.VERTICAL:
            if len(image.shape) == 2:  # 灰度图
                return image[start:end, :]
            elif len(image.shape) == 3:  # 彩色图
                return image[start:end, :, :]
            else:
                raise ValueError("Invalid image dimension, should be 2 or 3.")
    except IndexError:
        raise IndexError(
            QApplication.translate(
                "clip_image",
                "Clip index out of image bound. Index:{}, image_shape:{}, direction:{}",
            ).format(index, image.shape, direction.name)
        )
    else:
        return image  # 确保函数有显式返回值


@validate_call
def compare_image(
    image1: ImageArray,
    image2: ImageArray,
    method: ImageCompareMethod = ImageCompareMethod.SSIM,
) -> float:
    """比较两图片的差异，输入图像应为灰度图
    method="MSE" --- 均方差 Mean Squared Error (MSE), 0-65025, 数值越小越相似
    method="SSIM" --- 结构相似性指数 Structural Similarity Index (SSIM), 0-1, 数值越大越相似
    """
    image1 = np.asarray(image1, np.uint8)
    image2 = np.asarray(image2, np.uint8)
    if method == "MSE":
        diff = np.average((image1 - image2) ** 2)
    elif method == "SSIM":
        diff = ssim(image1, image2, data_range=255)
    else:
        raise ValueError("Invalid Compare Method.")
    if type(diff) is float or type(diff) is np.float64:
        return float(diff)
    else:
        raise TypeError("Comapre result is not float.")


@validate_call
def stitch_images(
    images: list[ImageArray], points: list[int], direction: Direction
) -> ImageArray:
    """将多张图像按指定方向和拼接点进行拼接"""
    if len(images) != len(points) + 1:
        raise ValueError(
            f"The image nums must be one greater than the stitching point nums. Got {len(images)} and {len(points)}"
        )

    match direction:
        case Direction.HORIZONTAL:
            image_clips = [images[0]] + [
                images[i + 1][:, points[i] :] for i in range(len(images) - 1)
            ]
            final_image = np.concatenate(image_clips, axis=1)  # 延水平方向拼接
        case Direction.VERTICAL:
            image_clips = [images[0]] + [
                images[i + 1][points[i] :, :] for i in range(len(images) - 1)
            ]
            final_image = np.concatenate(image_clips, axis=0)  # 延垂直方向拼接
    return final_image


@validate_call
def invert_image(img: ImageArray) -> ImageArray:
    return 255 - img
