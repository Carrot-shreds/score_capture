from typing import Literal, Optional

from PIL.Image import Image
import numpy as np
import cv2
from loguru import logger as log
from skimage.metrics import structural_similarity as compare_ssim

from data import Line, DATA, TYPE_IMAGE, ScoreDetections, ImageDetection

model = 0

def gama_transfer(img, threshold, power) -> np.ndarray:
    """对灰度图应用伽马转换，对灰度值除于阈值后进行幂运算，并线性映射到0-255范围"""
    img = np.power(img / threshold, power) * (np.power(255 / threshold, power) * threshold / 255)
    return np.asarray(np.round(img), np.uint8)

def detect_horizontal_lines(img: np.ndarray, coefficient:float = 0.5) -> list[Line]:
    """img为灰度图(二维数组)，识别并返回所有水平线段(白色背景图中的黑色线)"""
    if len(img.shape) != 2:
        log.warning("传入图像数组维度不为2，自动转换为灰度图，BGR2GRAY")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    if np.average(img) > 128:
        img = 255 - img  # 将图像反相为白底图
    average_row: np.ndarray = np.average(img, axis=1)  # 水平方向求平均值
    # slope: np.ndarray = average_row[1:] - average_row[:-1]  # 错位相减
    # slopes_slope = slope[1:] - slope[:-1]  # 斜率的斜率，鬼知道这玩意儿代表什么
    # result = slopes_slope - np.std(img, axis=1)[1:-1] / coefficient  # 消除短横线造成的抖动
    result = [r if (r - np.average(average_row))/np.std(average_row) > coefficient else 0 for r in average_row]  # 将小于0的值替换为0

    lines: list[Line] = []
    current_y: int = 1  # result比img短2个单位，等效于从img的1像素开始
    point_y: int = 0
    thickness: int
    for i in range(len(result)):
        if result[i] and (not point_y):  # 低于总体平均值时
            point_y = current_y
        elif not (result[i]) and point_y:
            thickness = current_y - point_y  # 计算线段厚度
            lines.append(Line((0, point_y), (len(img[0]) - 1, point_y),
                              thickness, direction="horizontal", image_shape=img.shape))
            point_y = 0
        current_y += 1
    if not lines:
        log.warning("水平线检测结果为空")
    return lines

def get_score_lines(horizontal_lines: list[Line]) -> list[Line]:
    """从水平线检测结果中获取曲谱部分的横线"""
    horizontal_lines_ys = np.asarray([line.point1[1] for line in horizontal_lines])
    distance = horizontal_lines_ys[1:] - horizontal_lines_ys[:-1]
    # if len(horizontal_lines) > 7 or np.std(distance) - np.average(distance, axis=0) > 0:
    #     index: np.ndarray = np.where(distance > np.average(distance))[0] + 1
    #     index: np.ndarray = np.sort(np.append(index, [0, len(horizontal_lines)]))
    #     index: list = [(int(index[i]), int(index[i + 1])) for i in range(np.shape(index)[0] - 1)]
    #     index: list = [i for i in index if (i[1] - i[0]) > 3]
    #     horizontal_lines: list[Line] = [horizontal_lines[i:j] for i, j in index][-1]
    index = np.argwhere((distance - np.average(distance, axis=0)) / np.std(distance) > 2) + 1
    index = np.sort(np.append(index, [0, len(horizontal_lines)]))
    index = [(int(index[i]), int(index[i + 1])) for i in range(np.shape(index)[0] - 1)]
    index = [i for i in index if (i[1] - i[0]) > 3]

    try:
        result = [horizontal_lines[i:j] for i, j in index][-1]
    except IndexError:
        log.warning("水平线检测结果中未找到曲谱部分的横线")
        return []
    return result

def detect_vertical_lines(img: np.ndarray, horizontal_lines: Optional[list[Line]] = None,
                          coefficient:float = 0.9) -> list[Line]:
    """img为灰度图(二维数组)，识别并返回所有竖直线段(黑色背景图中的白色线)"""
    # TODO 异常处理
    if len(img.shape) != 2:
        log.warning("传入图像数组维度不为2，自动转换为灰度图，BGR2GRAY")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    if np.average(img) > 128:
        img = 255 - img  # 将图像反相为黑底图

    if horizontal_lines is None:
        horizontal_lines: list[Line] = detect_horizontal_lines(img)
        log.warning("检测竖直线时未传入水平线数据，将先以默认系数进行水平线检测")
    if not horizontal_lines:
        log.warning("由于水平线检测结果为空，未进行竖直线检测")
        return []

    horizontal_lines = get_score_lines(horizontal_lines)  # 水平线预处理
    if not horizontal_lines:
        log.warning("曲谱部分的水平线检测结果为空，无法进行竖直线检测")
        return []

    # 识别区域
    top_line_y = horizontal_lines[0].start_pixel + 2  # 线谱中最上方的那条线，-2以确保包含线宽
    bottom_line_y = horizontal_lines[-1].end_pixel - 2  # 最下方的那条线
    edge_top: int = int(top_line_y - (bottom_line_y-top_line_y)/5)  # 上方延伸区域
    edge_bottom: int = int(bottom_line_y + (bottom_line_y-top_line_y)/5)  # 下方延伸区域
    edge_top = edge_top if edge_top > 0 else 0  # 限制上边界
    edge_bottom = edge_bottom if edge_bottom < img.shape[0] else img.shape[0] - 1  # 限制下边界

    # 初步识别
    sum_columns: np.ndarray = img[top_line_y:bottom_line_y].sum(axis=0)  # 线谱中的和
    sum_columns_ex: np.ndarray = img[edge_top:edge_bottom].sum(axis=0)  # 上下延伸一定范围的区域
    sum_columns: np.ndarray = np.asarray(  # 将小于均值的值置为0，以仅保留突出的数据影响
        [0 if s < np.average([np.max(sum_columns), np.min(sum_columns)]) else s for s in sum_columns])
    sum_columns_ex: np.ndarray = np.asarray(  # 同上
        [0 if s < np.average([np.max(sum_columns_ex), np.min(sum_columns_ex)]) else s for s in sum_columns_ex])
    bar_lines: np.ndarray = np.where(  # 确保竖直线段没有超出线谱范围
        (sum_columns / sum_columns.shape[0] - sum_columns_ex / sum_columns_ex.shape[0] * coefficient) > 0)[0]

    # # 去除上下不对称线段（上下段方差过大）
    # center_y = int(np.average([top_line_y, bottom_line_y]))
    # diff: list = [abs(np.average(img[top_line_y:center_y, i], axis=0) -
    #                   np.average(img[center_y:bottom_line_y, i], axis=0)
    #                   ) for i in bar_lines]
    # if np.std(diff) - np.average(diff, axis=0) > 0:  # 移除方差大于均值的线段
    #     del_index: list = [diff.index(d) for d in diff if d > np.average([np.max(diff), np.min(diff)])]
    #     bar_lines: np.ndarray = np.delete(bar_lines, del_index)

    # 去除长度/深度较低的线段
    # std = [np.std(img[top_line_y:bottom_line_y, i]) for i in bar_lines]
    # if np.max(std) - np.min(std) * 2 - np.average(std, axis=0) > 0:
    #     del_index = [std.index(s) for s in std if s > np.average(std)]
    #     bar_lines = np.delete(bar_lines, del_index)

    # 去除方差过大(上下不对称)的线段
    std_y:list[int] = [np.std(img[top_line_y:bottom_line_y, i], axis=0) for i in bar_lines]
    del_index:list[int] = [std_y.index(i) for i in std_y if  i > 35]  # 测试经验数值
    bar_lines: np.ndarray = np.delete(bar_lines, del_index)


    # 结构化存储结果
    index:np.ndarray = np.where(np.asarray(bar_lines[1:] - bar_lines[:-1]) != 1)[0] + 1
    index:np.ndarray = np.sort(np.append(index, [0, len(bar_lines)]))
    index_region:list[tuple[int, int]] = [(int(index[i]), int(index[i + 1])
                                           ) for i in range(np.shape(index)[0] - 1)]
    result:list = [bar_lines[i:j] for i, j in index_region]
    try:
        result = [Line((l[0], top_line_y), (l[0], bottom_line_y),
                    thickness=len(l), direction="vertical", image_shape=img.shape
                    ) for l in result]
    except IndexError:
        log.warning("竖直线检测结果中未找到曲谱部分的竖直线")
        return []
    return result

def detect_vertical_blanks(img: np.ndarray, horizontal_lines: Optional[list[Line]] = None,
                          coefficient:float = 0.8) -> list[Line]:
    """img为灰度图(二维数组)，识别并返回所有竖直线段(黑色背景图中的白色线)"""
    # TODO 未检测到线段时的异常处理
    if len(img.shape) != 2:
        log.warning("传入图像数组维度不为2，自动转换为灰度图，BGR2GRAY")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    if np.average(img) > 128:
        img = 255 - img  # 将图像反相为黑底图

    if horizontal_lines is None:
        horizontal_lines: list[Line] = detect_horizontal_lines(img)
        log.warning("检测竖直线时未传入水平线数据，将先以默认系数进行水平线检测")
    if not horizontal_lines:
        log.warning("由于水平线检测结果为空，未进行竖直线检测")
        return []

    horizontal_lines = get_score_lines(horizontal_lines)  # 水平线预处理

    # 初步识别
    top_line_y = horizontal_lines[0].start_pixel + 2  # 线谱中最上方的那条线，-2以确保包含线宽
    bottom_line_y = horizontal_lines[-1].end_pixel - 2  # 最下方的那条线
    edge_y: int = img.shape[0] - 2  # 图像底部边缘的坐标
    sum_columns: np.ndarray = img[top_line_y:bottom_line_y].sum(axis=0)  # 线谱中的和
    sum_columns_ex: np.ndarray = img[top_line_y:edge_y].sum(axis=0)  # 延伸到底部区域的和
    sum_columns: np.ndarray = np.asarray(  # 将小于均值的值置为0，以仅保留突出的数据影响
        [0 if s > np.average(sum_columns) else s for s in sum_columns])
    sum_columns_ex: np.ndarray = np.asarray(  # 同上
        [0 if s > np.average(sum_columns_ex) else s for s in sum_columns_ex])
    bar_lines: np.ndarray = np.where(  # 确保竖直线段没有超出线谱范围
        (sum_columns / sum_columns.shape[0] - sum_columns_ex / sum_columns_ex.shape[0] * 1) >= 0)[0]

    # std_y:list[int] = [np.std(img[top_line_y:bottom_line_y, i], axis=0) for i in bar_lines]
    # del_index:list[int] = [std_y.index(i) for i in std_y if  i > 35]
    # bar_lines: np.ndarray = np.delete(bar_lines, del_index)

    # 结构化存储结果
    index:np.ndarray = np.where(np.asarray(bar_lines[1:] - bar_lines[:-1]) != 1)[0] + 1
    index:np.ndarray = np.sort(np.append(index, [0, len(bar_lines)]))
    index_region:list[tuple[int, int]] = [(int(index[i]), int(index[i + 1])
                                           ) for i in range(np.shape(index)[0] - 1)]
    result:list = [bar_lines[i:j] for i, j in index_region]
    result = [Line((l[0], top_line_y), (l[0], bottom_line_y),
                   thickness=len(l), direction="vertical", image_shape=img.shape
                   ) for l in result]
    return result

def detect_all_lines_with_clip(img:np.ndarray, clip_length:int,
                               coefficient_horizontal:float, coefficient_vertical:float) -> tuple[list[Line], list[Line]]:
    """将图片以指定长度切片后，进行水平与竖直线段的检测"""
    if len(img.shape) != 2:
        log.warning("传入图像数组维度不为2，自动转换为灰度图，BGR2GRAY")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # 转换为灰度图

    lines = [[],[]]
    region:list[int] = [0, clip_length]
    while region[1] < (img.shape[1] - clip_length):
        if region[1] >= img.shape[1] - clip_length*2:
            clipped_image = img[:, region[0]:img.shape[1]]  # 保证最后一组长度clip_length<length<clip_length*2
        else:
            clipped_image = img[:, region[0]:region[1]]

        horizontal_lines = detect_horizontal_lines(clipped_image, coefficient_horizontal)
        for l in horizontal_lines: l.move_right(region[0], img.shape)  # 将线段向右移动指定像素值
        try:
            vertical_lines = detect_vertical_lines(clipped_image, horizontal_lines, coefficient_vertical)
        except IndexError:
            vertical_lines = []
        for l in vertical_lines: l.move_right(region[0], img.shape)

        lines[0] += horizontal_lines
        lines[1] += vertical_lines
        region[0] += clip_length
        region[1] += clip_length

    return lines[0], lines[1]

def get_barline_num_region(image_detection: ImageDetection) -> tuple[int, int]:
    """获取图片上半区域中，小节数上下的区域，用以对该区域加权计算"""
    point1_y = image_detection.vertical_lines[0].point1[1]  # 小节线的上方点y
    point2_y = image_detection.vertical_lines[0].point2[1]
    detect_width = abs(point2_y - point1_y)
    detect_start = int(point1_y - detect_width / 2)
    detect_start = detect_start if detect_start >= 0 else 0  # 防止出现负数
    detect_end = int(point1_y + detect_width / 2)
    return detect_start, detect_end

def image_pre_process(img: TYPE_IMAGE | Image, data: DATA) -> np.ndarray:
    """图像预处理"""
    img = np.array(img, np.uint8)
    if data.if_reverse_image:
        img = 255 - img
    # img = super_resolution(img)
    return img

def super_resolution(image: TYPE_IMAGE) -> TYPE_IMAGE:
    global model
    if not model:
        model = cv2.dnn_superres.DnnSuperResImpl.create()
        model.readModel(r"./resource/superres_model/ESPCN_x2.pb")
        model.setModel("espcn", 2)
    return model.upsample(image)

def clip_image(image: TYPE_IMAGE,direction:Literal["horizontal", "vertical"],
                index:tuple[int|None, int|None]) -> TYPE_IMAGE:
    """按指定方向和索引对图像进行切片, (1,None)表示[1:]]"""
    if direction not in ["horizontal", "vertical"]:
        raise ValueError("direction must be 'horizontal' or 'vertical'")
    
    start, end = index

    try:
        if direction == "horizontal":
            if len(image.shape) == 2:  # 灰度图
                return image[:, start:end]
            elif len(image.shape) == 3:  # 彩色图
                return image[:, start:end, :]
            else:
                raise ValueError("图像维度不正确，应为2或3维")
        if direction == "vertical":
            if len(image.shape) == 2:  # 灰度图
                return image[start:end, :]
            elif len(image.shape) == 3:  # 彩色图
                return image[start:end, :, :]
            else:
                raise ValueError("图像维度不正确，应为2或3维")
    except IndexError:
        raise IndexError("切片范围超出图像范围，请检查index参数")

def read_image(filepath: str, color: Literal["RGB", "BGR", "GRAY"] = "RGB") -> TYPE_IMAGE:
    """支持中文路径的cv图片读取"""
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), -1)
    if color == "RGB":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if color == "GRAY":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img

def save_image(filepath: str, img: TYPE_IMAGE) -> None:
    """支持中文路径的cv图片存储"""
    image_format = "." + filepath.split(".")[-1]  # 获取文件格式
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imencode(f"{image_format}", np.asarray(img))[1].tofile(filepath)

def compare_image(image1: TYPE_IMAGE, image2: TYPE_IMAGE, method: Literal["SSIM", "MSE"] = "SSIM") -> float:
    """ 比较两图片的差异，输入图像应为灰度图
        method="MSE" --- 均方差 Mean Squared Error (MSE), 0-65025, 数值越小越相似
        method="SSIM" --- 结构相似性指数 Structural Similarity Index (SSIM), 0-1, 数值越大越相似
    """
    if method == "MSE":
        diff = np.sum((image1.flatten() - image2.flatten()) ** 2) / image1.size
    elif method == "SSIM":
        diff = compare_ssim(image1, image2, data_range=255)
    else:
        raise ValueError("错误的算法类型")
    return diff
