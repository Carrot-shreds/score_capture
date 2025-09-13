import pickle
import json
import sys
from typing import Optional, Literal, Any

from loguru import logger as log
import cv2
import numpy as np
from PySide6.QtCore import QRect
import pyautogui

from config import Config
from utilities import order_filenames, hash_image

TYPE_IMAGE = np.ndarray | cv2.UMat | np.ndarray[Any, np.dtype]
LITERAL_COMPARE_METHODS = Literal["SSIM", "MSE"]
LITERAL_DETECT_METHODS = Literal["SSIM", "MSE"]
LITERAL_STITCH_METHODS = Literal["DIRECT", "SSIM", "MSE"]
LITERAL_DIRECTIONS = Literal["horizontal", "vertical"]

class DATA:
    """
    数据管理类，存储所有数据与配置，及相关更新函数
    数据初始化主要在UI.__init__()中
    """

    def __init__(self, window_region=(0, 0, 0, 0)):
        self.exe_path = sys.argv[0]
        self.ini_file = self.exe_path + "\\config.ini"

        self.SCREEN_SIZE: tuple[int, int] = pyautogui.size()  # （width，height）
        self.WINDOW_GEOMETRY: tuple[int, int, int, int] = window_region  # 主窗口几何属性（x,y,宽，高）

        # 全局设置
        self.score_save_path: str = self.exe_path + "\\output"  # 保存文件夹目录
        self.working_path: str = self.score_save_path  # 当前曲谱工作目录
        self.score_title: str = "untitled"
        self.score_save_format: str = ".jpg"
        self.log_output_level = "DEBUG"
        self.always_on_top: bool = True

        # 定位设置
        self.region:Region = Region(0,0,114,511)  # 截图范围，（x，y，w，h）

        # 截图设置
        self.compare_method: LITERAL_COMPARE_METHODS = "SSIM"
        self.compare_threshold: float = 0.96
        self.capture_delay: float = 0.7  # 延时时间，单位(秒/)
        self.if_keep_last: bool = True
        self.if_reverse_image: bool = False

        # 拼接设置
        self.stitch_method: LITERAL_STITCH_METHODS = "MSE"
        self.stitch_direction: LITERAL_DIRECTIONS = "horizontal"

        # 检测算法设置
        self.detect_coefficient_horizontal: float = 0.7
        self.detect_coefficient_vertical: float = 0.8

        # 分割设置
        self.reclip_method: int = 1  # 0:每行固定小节数 1:填充每行最大长度
        # 样式设置
        self.clip_align: int = 0  # 每行切片位置 0：靠左，1：居中，2：靠右

        # 配置设置
        self.if_auto_manage_config: bool = True

        # # 图像识别设置
        # self.horizontal_lines_num: int = 6
        # self.bar_lines_num: int = 0

        # log config
        self.log_output_color: dict[str, str] = {  # log level与其对应的输出颜色
            "DEBUG": "grey",
            "INFO": "black",
            "SUCCESS": "green",
            "WARNING": "orange",
            "ERROR": "red"
        }

        self.image_preview: np.ndarray = np.ndarray([])
        self.lines_detections: dict[str, str|dict[str, list[Line]]] = {  # 定义数据结构
            # "path": "",
            # "filename": {
            #     "horizontal_lines": list[Line],
            #     "vertical_lines": list[Line]
            # }
        }

        self.config = Config(self)


class Region:
    """
    管理坐标范围数据
    """

    def __init__(self, x:int, y:int, width:int, height:int) -> None:
        self.x:int = x
        self.y:int = y
        self.width:int = width
        self.height:int = height


    def set(self, region:tuple[int, int, int, int] | np.ndarray | list[int]) -> None:
        """更新坐标值"""
        self.x = region[0]
        self.y = region[1]
        self.width = region[2]
        self.height = region[3]

    def set_from_geometry(self, geo:QRect) -> None:
        self.set(self.geometry_to_region(geo))

    def get_tuple(self) -> tuple[int, int, int, int]:
        """获取列表形式"""
        return self.x, self.y, self.width, self.height

    def __getitem__(self, key):
        """实现[key]形式访问region中的值"""
        match key:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.width
            case 3:
                return self.height
        raise IndexError("region index out of range, must in [0-3]")

    def get_array(self) -> np.ndarray:
        """获取数组形式"""
        return np.asarray(self.get_tuple())

    def region_to_geometry(self, without_title_frame=False) -> QRect:
        """四元组（x,y_sin,宽,高）转换为QRect对象"""
        if without_title_frame:
            self.height -= 30  # 减去标题栏高度
            self.y -= 1  # 减去1px阴影
        return QRect(self.x, self.y, self.width, self.height)

    @staticmethod
    def geometry_to_region(geometry: QRect) -> tuple[int, int, int, int]:
        """转换QRect为（x,y,w,h）四元组"""
        return (geometry.x(), geometry.y(), geometry.width(), geometry.height())


class Line:
    """线段类，存储起始线段的坐标，以及在对应方向上的厚度"""

    def __init__(self,
                 point1: tuple[int, int],
                 point2: tuple[int, int],
                 thickness: int,  # 在水平或竖直方向上的厚度，即从1开始， 不为零
                 direction: LITERAL_DIRECTIONS,  # 线段延水平/竖直方向
                 image_shape: tuple[int, int]  # 图像的尺寸，（height， width）
                 ) -> None:
        self.point1: tuple[int, int] = point1
        self.point2: tuple[int, int] = point2
        self.thickness: int = thickness
        self.direction: LITERAL_DIRECTIONS = direction
        self.image_shape:tuple[int, int] = image_shape
        self.start_pixel: int = 0  # 在set_thickness中设置
        self.end_pixel: int = 0  # 水平或竖直方向上，起始点的坐标索引
        self.set_thickness(self.thickness)

    def set_thickness(self, thickness: int) -> None:
        self.thickness = thickness
        if self.direction == "horizontal":
            self.start_pixel = self.point1[1]
            self.end_pixel = self.point1[1] + self.thickness - 1
        if self.direction == "vertical":
            self.start_pixel = self.point1[0]
            self.end_pixel = self.point1[0] + self.thickness - 1

    def draw(self, img: TYPE_IMAGE, color: tuple[int, int, int] = (0, 255, 0)) -> None:
        """
        绘制线段到输入图像
        :param img: 要绘制的原始图像
        :param color: 绘制颜色，BGR色彩，默认值为绿色
        """
        point1 = list(self.point1)
        point2 = list(self.point2)
        for i in range(self.thickness):
            cv2.line(img, point1, point2, color, thickness=1)
            if self.direction == "horizontal":
                point1[1] += 1
                point2[1] += 1
            if self.direction == "vertical":
                point1[0] += 1
                point2[0] += 1

    def get_index_points(self, extern_width:int = 0, reverse:bool=False) -> np.ndarray:
        """获取线段在相应方向上的索引值，并相周围扩展额外的像素值"""
        point1 = list(self.point1)
        point1[0] -= extern_width if point1[0] >= extern_width else 0  # 避免出现负数
        point1[1] -= extern_width if point1[0] >= extern_width else 0
        thickness = self.thickness + int(extern_width*2)
        index_points = []
        for i in range(thickness):
            if self.direction == "horizontal":
                index_points.append(point1[1])
                point1[1] += 1
            if self.direction == "vertical":
                index_points.append(point1[0])
                point1[0] += 1
        index_points = np.asarray(index_points)
        edge =  self.image_shape[0] if self.direction == "horizontal" else self.image_shape[1]
        index_points= np.delete(index_points, np.argwhere(index_points > edge))
        if reverse:
            index_points = edge - index_points  # 翻转索引值正方向
        return index_points

    def move_right(self, pixel:int, image_shape:Optional[tuple[int, int]]) -> None:
        """将线段延水平方向移动指定像素，向右为正"""
        point1, point2 = list(self.point1), list(self.point2)
        point1[0] += pixel
        point2[0] += pixel
        image_shape = image_shape if image_shape is not None else self.image_shape
        if not(0<=point1[0]<=image_shape[1] and 0<=point2[0]<=image_shape[1]):
            raise ValueError("move pixel out of image shape region")  # 线段移动后超出图像范围
        self.__init__(point1=(point1[0], point1[1]),
                      point2=(point2[0], point2[1]),
                      thickness=self.thickness,
                      direction=self.direction,
                      image_shape=image_shape)

class CaptureData:
    """
    截图数据类，存储截图的相关比对数据
    """

    def __init__(self, data={}) -> None:
        self.data: dict[frozenset[str],  # 两张图像的文件名，set不可hash，不能作为键值
                         dict[str, float]] = data  # 对比结果，算法：数值

    def add_diff(self, image1:str, image2:str, 
                 compare_method:LITERAL_COMPARE_METHODS, diff:float) -> None:
        """添加比对结果"""
        image_couple = frozenset((image1, image2))
        if not self.data.get(image_couple):  # 如果图像数据为空
            self.data[image_couple] = {compare_method: diff}
        else:
            self.data[image_couple][compare_method] = diff

    def get_image_sequence(self) -> list[str]:
        """获取所有图像的名称列表"""
        image_names = []
        for k in self.data.keys():
            image_names += list(k)
        image_names = set(image_names)  # 去重
        image_names = order_filenames(list(image_names))
        return image_names
    
    def get_diff(self, image1:str, image2:str, 
                 compare_method:LITERAL_COMPARE_METHODS) -> float | None:
        """获取两图片的比对结果"""
        image_couple = frozenset([image1, image2])
        image = self.data.get(image_couple)
        if image:
            diff = image.get(compare_method)
        else:
            diff = None
        return diff
    
    def get_diff_sequence(self, compare_method:LITERAL_COMPARE_METHODS, 
                          image_names: list[str]) -> list[float]:
        if not image_names:
            image_names = self.get_image_sequence()
        image_names = order_filenames(image_names)
        diff_sequence: list[float] = []
        for n in range(len(image_names)-1):
            image_couple = frozenset([image_names[n], image_names[n+1]])
            img = self.data.get(image_couple)
            if not img:
                log.error(f"未找到{image_names[n]}|{image_names[n+1]}图像的比对信息")
                return []
            diff = img.get(compare_method)
            if not diff:
                log.error(f"未找到{image_names[n]}|{image_names[n+1]}的{compare_method}算法差异值")
                return []
            diff_sequence.append(diff)
        return diff_sequence
    
    def save_to_file(self, file:str) -> None:
        """保存比对数据到文件"""
        data: dict = {}
        for k in self.data.keys():
            image_names = order_filenames(list(k))
            data[f"{image_names[0]} | {image_names[1]}"] = self.data[k]  # 将键值从set转换为str
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
    @staticmethod
    def load_from_file(file:str) -> "CaptureData":
        """从文件中加载比对数据"""
        with open(file, "r") as f:
            load: dict = json.load(f)
            data = {frozenset((k.split("|")[0].strip(), k.split("|")[1].strip())):load[k]
                     for k in load.keys()}  # 将键值从str转换回set
            return CaptureData(data)


class ImageDetection:
    def __init__(self, path:str, filename:str,
                 horizontal_lines:list[Line], vertical_lines:list[Line]) -> None:
        self.path = path
        self.filename = filename
        self.horizontal_lines = horizontal_lines
        self.vertical_lines = vertical_lines
        self.image_shape = self.horizontal_lines[0].image_shape

    def get_lines(self, direction:LITERAL_DIRECTIONS="vertical") -> list[Line]:
        """获取指定方向的线段列表"""
        if direction == "horizontal":
            return self.horizontal_lines
        elif direction == "vertical":
            return self.vertical_lines
        else:
            raise ValueError("direction must be 'horizontal' or 'vertical'")

    def get_lines_index(self,
                        direction:LITERAL_DIRECTIONS="vertical",
                        extern_width:int = 5,
                        reverse=False,
                        ) -> np.ndarray:
        "获取指定方向的线段索引值"
        lines = self.horizontal_lines if direction == "horizontal" else self.vertical_lines
        points = np.concatenate([line.get_index_points(extern_width=extern_width, reverse=reverse
                                                    ) for line in lines])
        return points


class ScoreDetections:
    def __init__(self, path:str, title:str) -> None:
        self.path = path
        self.title = title
        self.images:dict[str, ImageDetection] = {
            # "image0.jpg": ImageDetection(self.path, "image0.jpg")
        }

    def add_image(self, filename:str,
                  horizontal_lines:list[Line], vertical_lines:list[Line]) -> None:
        self.images[filename] = ImageDetection(self.path, filename,
                                               horizontal_lines, vertical_lines)

    def get_image_filenames(self) -> list[str]:
        """获取所有的图像名称"""
        return [k for k in self.images.keys()]

    def __getitem__(self, key) -> ImageDetection:
        if type(key) is str:
            result = self.images.get(key)
        elif type(key) is int:
            result = self.images.get(self.get_image_filenames()[key])
        else:
            raise TypeError(f"错误的索引类型{type(key)}")
        
        if result is None:
            raise KeyError(f"未找到图像{key}的检测结果")
        else:
            return result

    # noinspection PyTypeChecker
    def save_to_file(self, file) -> None:
        """保存到文件中"""
        with open(file, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(file) -> "ScoreDetections":
        """从文件中读取"""
        with open(file, "rb") as f:
            return pickle.load(f)

class StitchData:
    """存储拼接点数据"""
    def __init__(self, points: list[int], images: list[np.ndarray] | None, stitch_direction) -> None:

        self.stitch_direction: LITERAL_DIRECTIONS = stitch_direction
        self.stitch_config:dict[str, str] = {
            "stitch_direction": self.stitch_direction
        }

        self.points:list[int] = points
        if images and self.points and len(images) != len(self.points)+1:
            raise ValueError("图像数量必须比拼接点数量多1")
        if images is None:
            self.image_hashes:list[str] = ["No image hash input!" for i in range(len(self.points)+1)]
            self.image_shapes: list[tuple[int, int]] = [(0,0) for i in range(len(self.points)+1)]
        else:
            self.image_hashes:list[str] = [hash_image(img) for img in images]
            self.image_shapes: list[tuple[int, int]] = [img.shape for img in images]

    def add_point(self, point:int, image:tuple[np.ndarray, np.ndarray]) -> None:
        """添加拼接点和对应的图像"""
        self.points.append(point)
        self.image_hashes.append(hash_image(image[0]))
        self.image_hashes.append(hash_image(image[1]))

    def save_to_file(self, file: str) -> None:
        """保存比对数据到文件"""
        config: dict = self.stitch_config
        points: dict = {i:{"stitchpoint":self.points[i],
                         "image1": {
                             "shape":self.image_shapes[i],
                             "hash":self.image_hashes[i]
                             },
                         "image2": {
                             "shape":self.image_shapes[i+1],
                             "hash":self.image_hashes[i+1]
                             },
                         } for i in range(len(self.points))}
        data: dict = {
            "StitchConfig": config,
            "StitchPoints": points
        }
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_from_file(file: str) -> "StitchData":
        """从文件中加载比对数据"""
        with open(file, "r") as f:
            load: dict = json.load(f)
            dict_config: dict = load["StitchConfig"]
            dict_points: dict = load["StitchPoints"]
            points = [dict_points[str(i)]["stitchpoint"] for i in range(len(dict_points.keys()))]
            image_shapes = [dict_points[str(i)]["image1"]["shape"] for i in range(len(dict_points.keys()))]
            image_shapes.append(dict_points[str(len(dict_points.keys())-1)]["image2"]["shape"])
            image_hashes = [dict_points[str(i)]["image1"]["hash"] for i in range(len(dict_points.keys()))]
            image_hashes.append(dict_points[str(len(dict_points.keys())-1)]["image2"]["hash"])
            data = StitchData(points, None, stitch_direction=dict_config["stitch_direction"])
            data.image_shapes = image_shapes
            data.image_hashes = image_hashes
            return data
        
    def __eq__(self, value: "StitchData") -> bool:
        if self.image_hashes == value.image_hashes and self.stitch_config == value.stitch_config:
            return True
        else:
            return False
