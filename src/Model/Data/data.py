import json

import numpy as np
from loguru import logger as log
from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeInt,
    PositiveInt,
    validate_call,
)

from src.Model.Data.const import Direction, ImageCompareMethod
from src.Model.Data.settings import StitchSettings
from src.Model.Data.type import (
    AlwaysValidateModel,
    Directory,
    ImageFileName,
    JsonPath,
    Line,
    NonEmptyStr,
    OnValueChangeModel,
    ZeroToOneOpen,
)
from src.Model.utils import hash_image, order_filenames


class ImageData(BaseModel):
    model_config = ConfigDict(
        frozen=True,
    )
    filename: ImageFileName
    shape: tuple[PositiveInt, PositiveInt]
    hash: NonEmptyStr

    def __init__(
        self,
        filename: ImageFileName,
        shape: tuple[PositiveInt, PositiveInt] | None = None,
        hash: NonEmptyStr | None = None,
        image: np.ndarray | None = None,
    ):
        if shape and hash:
            super().__init__(filename=filename, shape=shape, hash=hash)
        elif image is not None:
            super().__init__(
                filename=filename,
                shape=(image.shape[0], image.shape[1]),
                hash=hash_image(image),
            )
        else:
            raise ValueError("Invalid ImageData parameter")

    @property
    def file_extension(self):
        return ("." + self.filename.split(".")[-1]).lower()

    @property
    def filename_without_extension(self):
        return self.filename.split("." + self.filename.split(".")[-1])[0]


class CaptureData(BaseModel):
    """
    截图数据类，存储截图的相关比对数据
    """

    data: dict[
        frozenset[ImageFileName],  # 两张图像的文件名，set不可hash，不能作为键值
        dict[str, float],  # 对比结果，算法：数值
    ] = {}

    @validate_call
    def add_diff(
        self,
        image1: ImageFileName,
        image2: ImageFileName,
        compare_method: ImageCompareMethod,
        diff: float,
    ) -> None:
        """添加比对结果"""
        image_couple = frozenset((image1, image2))
        if not self.data.get(image_couple):  # 如果图像数据为空
            self.data[image_couple] = {compare_method: diff}
        else:
            self.data[image_couple][compare_method] = diff

    def get_image_sequence(self) -> list[ImageFileName]:
        """获取所有图像的名称列表"""
        image_names = []
        for k in self.data.keys():
            image_names += list(k)
        image_names = set(image_names)  # 去重
        return order_filenames(list(image_names))

    @validate_call
    def get_diff(
        self,
        image1: ImageFileName,
        image2: ImageFileName,
        compare_method: ImageCompareMethod,
    ) -> float | None:
        """获取两图片的比对结果"""
        image_couple = frozenset([image1, image2])
        image_data = self.data.get(image_couple)
        if image_data:
            diff = image_data.get(compare_method)
        else:
            diff = None
        return diff

    @validate_call
    def get_diff_sequence(
        self, compare_method: ImageCompareMethod, image_names: list[ImageFileName]
    ) -> list[float]:
        if not image_names:
            image_names = self.get_image_sequence()
        else:
            image_names = order_filenames(image_names)

        diff_sequence: list[float] = []
        for n in range(len(image_names) - 1):
            image_couple = frozenset([image_names[n], image_names[n + 1]])
            img_data = self.data.get(image_couple)
            if not img_data:
                log.warning(
                    f"No compare data found for {image_names[n]}|{image_names[n + 1]}"
                )
                return []
            diff = img_data.get(compare_method)
            if not diff:
                log.warning(
                    f"No compare data found with {compare_method} method for {image_names[n]}|{image_names[n + 1]}"
                )
                return []
            diff_sequence.append(diff)
        return diff_sequence

    @validate_call
    def save_to_file(self, file: JsonPath) -> None:
        """保存比对数据到文件"""
        save_dict: dict = {}
        for k in self.data.keys():
            image_names = order_filenames(list(k))
            save_dict[f"{image_names[0]} | {image_names[1]}"] = self.data[
                k
            ]  # 将键值从set转换为str
        with open(file, "w", encoding="utf-8") as f:
            json.dump(save_dict, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_from_file(file: JsonPath) -> "CaptureData":
        """从文件中加载比对数据"""
        with open(file, "r", encoding="utf-8") as f:
            load: dict = json.load(f)
            data = {
                frozenset((k.split("|")[0].strip(), k.split("|")[1].strip())): load[k]
                for k in load.keys()  # 将键值从str转换回set
            }
            return CaptureData(data=data)


class ImageDetection(BaseModel):
    image_data: ImageData
    horizontal_lines: list[Line] = []
    vertical_lines: list[Line] = []

    @property
    def image_shape(self) -> tuple[int, int]:
        return self.image_data.shape

    @validate_call
    def add_line(self, line: Line, direction: Direction) -> None:
        if line.image_shape != self.image_data.shape:
            raise ValueError(
                "Shape of the image is different between ImageDetection and the Line"
            )
        match direction:
            case Direction.HORIZONTAL:
                self.horizontal_lines.append(line)
            case Direction.VERTICAL:
                self.vertical_lines.append(line)

    @validate_call
    def get_lines(self, direction: Direction = Direction.VERTICAL) -> list[Line]:
        """获取指定方向的线段列表"""
        match direction:
            case Direction.HORIZONTAL:
                return self.horizontal_lines
            case Direction.VERTICAL:
                return self.vertical_lines
        raise ValueError("Undefined direction")

    @validate_call
    def get_lines_index(
        self,
        direction: Direction = Direction.VERTICAL,
        extern_width: PositiveInt = 5,
        reverse=False,
    ) -> np.ndarray:
        """获取指定方向的线段索引值"""
        lines = self.get_lines(direction)
        if lines is None or lines == []:
            return np.array([])
        points = np.concatenate(
            [
                line.get_index_points(extern_width=extern_width, reverse=reverse)
                for line in lines
            ]
        )
        return points


class ScoreDetections(BaseModel):
    directory: Directory
    image_detections: dict[ImageFileName, ImageDetection] = {}

    @property
    def image_shape(self) -> tuple[PositiveInt, PositiveInt] | None:
        if self.image_detections:
            return list(self.image_detections.values())[0].image_shape
        else:
            return None

    @validate_call
    def add_image(
        self,
        image_data: ImageData,
        horizontal_lines: list[Line],
        vertical_lines: list[Line],
    ) -> None:
        self.image_detections[image_data.filename] = ImageDetection(
            image_data=image_data,
            horizontal_lines=horizontal_lines,
            vertical_lines=vertical_lines,
        )

    def get_image_filenames(self) -> list[str]:
        """获取所有的图像名称"""
        return list(self.image_detections.keys())

    def __getitem__(self, key: str | int) -> ImageDetection:
        if type(key) is str:
            result = self.image_detections.get(key)
        elif type(key) is int:
            result = self.image_detections.get(self.get_image_filenames()[key])
        else:
            raise TypeError(f"Invalid index type {type(key)}")

        if result is None:
            raise KeyError(f"No detection data found for {key}")
        else:
            return result

    def save_to_file(self, file: JsonPath) -> None:
        """保存到文件中"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4, ensure_ascii=False))

    @staticmethod
    def load_from_file(file: JsonPath) -> "ScoreDetections":
        """从文件中读取"""
        with open(file, "r", encoding="utf-8") as f:
            model = ScoreDetections.model_validate_json(f.read())
            if model.directory != file.parent:  # update model directory
                model.directory = file.parent
            return model


class ImageStitchData(BaseModel):
    stitch_point: NonNegativeInt
    image1: ImageData
    image2: ImageData


class ScoreStitchData(BaseModel):
    """存储拼接点数据"""

    stitch_settings: StitchSettings
    data: dict[int, ImageStitchData] = {}

    @property
    def stitch_points(self) -> list[int]:
        return [d.stitch_point for d in self.data.values()]

    @property
    def image_stitch_data(self) -> list[ImageStitchData]:
        keys = list(self.data.keys())
        keys.sort()
        return [self.data[k] for k in keys]

    @property
    def image_hashes(self) -> list[str]:
        return [d.image1.hash for d in self.image_stitch_data] + [
            self.image_stitch_data[-1].image2.hash
        ]

    @property
    def image_shapes(self) -> list[tuple[int, int]]:
        return [d.image1.shape for d in self.image_stitch_data] + [
            self.image_stitch_data[-1].image2.shape
        ]

    @validate_call(config=ConfigDict(arbitrary_types_allowed=True))
    def add_points(
        self, points: list[int], images: list[np.ndarray], image_names: list[str]
    ) -> None:
        if not len(points) + 1 == len(images) == len(image_names):
            raise ValueError(
                "The length of stitch_point, images and image_names are not matched"
            )
        for i in range(len(points)):
            image1_data = ImageData(filename=image_names[i], image=images[i])
            image2_data = ImageData(filename=image_names[i + 1], image=images[i + 1])
            self.add_point(points[i], image1_data, image2_data)

    @validate_call
    def add_point(
        self, point: int, image1_data: ImageData, image2_data: ImageData
    ) -> None:
        """添加拼接点和对应的图像"""
        if point > image2_data.shape[self.stitch_settings.direction]:
            raise ValueError(
                f"stitch_point index {point} out of image bounds: shape{image2_data.shape}"
            )
        image_stitch_data = ImageStitchData(
            stitch_point=point,
            image1=image1_data,
            image2=image2_data,
        )
        self.data[len(self.data.keys())] = image_stitch_data

    def save_to_file(self, file: JsonPath) -> None:
        """保存到文件中"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4, ensure_ascii=False))

    @staticmethod
    def load_from_file(file: JsonPath) -> "ScoreStitchData":
        """从文件中读取"""
        with open(file, "r", encoding="utf-8") as f:
            return ScoreStitchData.model_validate_json(f.read())


class ReclipData(BaseModel):
    """
    分割数据类，存储分割的相关数据
    """

    clip_direction: Direction
    clip_indexes: list[tuple[int, int]]
    clip_height: int | None = None

    def save_to_file(self, file: JsonPath) -> None:
        """保存到文件中"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4, ensure_ascii=False))

    @staticmethod
    def load_from_file(file: JsonPath) -> "ReclipData":
        """从文件中读取"""
        with open(file, "r", encoding="utf-8") as f:
            return ReclipData.model_validate_json(f.read())


class StyleData(AlwaysValidateModel, OnValueChangeModel):
    """
    样式数据类，存储样式的相关数据
    """

    title: str = "Untitled"
    margin_width: ZeroToOneOpen = 0.08
    margin_height: ZeroToOneOpen = 0.08
    margin_title: ZeroToOneOpen = 0.13
    add_title: bool = True
    add_page_num: bool = True

    def save_to_file(self, file: JsonPath) -> None:
        """保存到文件中"""
        with open(file, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4, ensure_ascii=False))

    @staticmethod
    def load_from_file(file: JsonPath) -> "StyleData":
        """从文件中读取"""
        with open(file, "r", encoding="utf-8") as f:
            return StyleData.model_validate_json(f.read())
