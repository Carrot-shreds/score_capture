import pickle
import sys
from typing import Optional, Literal, overload, Any

from loguru import logger as log
import cv2
import numpy as np
from PySide6.QtCore import QRect
import pyautogui

from config import Config

TYPE_IMAGE = np.ndarray | cv2.UMat | np.ndarray[Any, np.dtype]


class DATA:
    """
    数据管理类，存储所有数据与配置，及相关更新函数
    数据初始化主要在UI.__init__()中
    """

    def __init__(self, window_region=(0, 0, 0, 0)):
        self.exe_path = sys.argv[0]
        self.ini_file = self.exe_path + "\\config.ini"

        self.SCREEN_SIZE: (int, int) = pyautogui.size()  # （width，height）
        self.WINDOW_GEOMETRY: (int, int, int, int) = window_region  # 主窗口几何属性（x,y,宽，高）

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
        self.compare_method: Literal["SSIM", "MSE"] = "SSIM"
        self.compare_threshold: float = 0.9
        self.capture_delay: float = 0.7  # 延时时间，单位(秒/)
        self.if_keep_last: bool = True
        self.if_reverse_image: bool = False

        # 拼接设置
        self.stitch_method: Literal["SSIM", "MSE"] = "MSE"

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

        self.image_preview: TYPE_IMAGE = np.ndarray([])
        self.lines_detections: dict[str:str, str:dict[str:list[Line]]] = {  # 定义数据结构
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


    def set(self, region:tuple[int, int, int, int] | np.ndarray) -> None:
        """更新坐标值"""
        self.x = region[0]
        self.y = region[1]
        self.width = region[2]
        self.height = region[3]

    def set_from_geometry(self, geo:QRect) -> None:
        self.set(self.geometry_to_region(geo))

    def tuple(self) -> tuple[int, int, int, int]:
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

    def array(self) -> np.ndarray:
        """获取数组形式"""
        return np.asarray(self.tuple())

    def region_to_geometry(self) -> QRect:
        """四元组（x,y_sin,宽,高） -> x,y加上offset -> 高度减去标题栏的30px -> [x,y,宽,高]"""
        return QRect(self.x, self.y, self.width, self.height)

    @staticmethod
    def geometry_to_region(geometry: QRect) -> (int, int, int, int):
        """转换QRect为（x,y,w,h）四元组"""
        return np.asarray((geometry.x(), geometry.y(),
                           geometry.width(), geometry.height()))

class Line:
    """线段类，存储起始线段的坐标，以及在对应方向上的厚度"""

    def __init__(self,
                 point1: tuple[int, int],
                 point2: tuple[int, int],
                 thickness: int,  # 在水平或竖直方向上的厚度，即从1开始， 不为零
                 direction: Literal["horizontal", "vertical"],  # 线段延水平/竖直方向
                 image_shape: tuple  # 图像的尺寸，（height， width）
                 ) -> None:
        self.point1 = point1
        self.point2 = point2
        self.thickness = thickness
        self.direction = direction
        self.image_shape = image_shape
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



class ImageDetection:
    def __init__(self, path:str, filename:str,
                 horizontal_lines:list[Line], vertical_lines:list[Line]) -> None:
        self.path = path
        self.filename = filename
        self.horizontal_lines = horizontal_lines
        self.vertical_lines = vertical_lines
        self.image_shape = self.horizontal_lines[0].image_shape

    def get_lines_index(self,
                        direction:Literal["horizontal", "vertical"]="vertical",
                        extern_width:int = 5,
                        reverse=False,
                        ) -> np.ndarray:
        lines = self.horizontal_lines if direction == "horizontal" else self.vertical_lines
        points = np.concatenate([l.get_index_points(extern_width=extern_width, reverse=reverse
                                                    ) for l in lines])
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
        if type(key) == str:
            return self.images.get(key)
        elif type(key) == int:
            return self.images.get(self.get_image_filenames()[key])
        else:
            raise KeyError(key)

    # noinspection PyTypeChecker
    def save_to_file(self, file) -> None:
        """保存到文件中"""
        with open(file, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(file):
        """从文件中读取"""
        with open(file, "rb") as f:
            return pickle.load(f)
