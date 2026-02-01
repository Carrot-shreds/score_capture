import contextlib
import sys
import threading
from copy import deepcopy
from pathlib import Path
from typing import Annotated, Any, Callable, Optional, Self

import cv2
import mss
import numpy as np
from annotated_types import Ge, Gt, Le, Lt
from loguru import logger as log
from numpydantic import NDArray, Shape
from pathvalidate import (
    is_valid_filename,
    is_valid_filepath,
    sanitize_filename,
    sanitize_filepath,
)
from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    GetPydanticSchema,
    NonNegativeInt,
    PositiveInt,
    ValidationError,
    model_validator,
)
from pydantic_extra_types.color import Color

from src.Model.Data.const import IMAGE_EXTENSIONS, Direction

###########################################################
# Annotated types
###########################################################
# Basic #########################################
type NonEmptyStr = Annotated[str, Field(min_length=1)]


# Validators ################
def filename_validator(value: NonEmptyStr) -> NonEmptyStr:
    if is_valid_filename(value, platform=sys.platform):
        return value
    else:
        sanitized_value = sanitize_filename(value, platform=sys.platform)
        log.warning(
            f"Invalid filename: {value}, automatically fix to {sanitized_value}"
        )
        return sanitized_value


def filename_extension_validator(
    value: NonEmptyStr | Path, extensions: tuple[str, ...]
) -> NonEmptyStr | Path:
    if isinstance(value, str):
        extension = "." + value.split(".")[-1]  # pyright:ignore
    elif isinstance(value, Path):
        extension = "." + value.name.split(".")[-1]  # pyright:ignore
    else:
        raise ValueError("value must be str or path")
    if extension not in extensions:
        raise ValueError(f"Wrong file extension:{extension}, expect for:{extensions}")
    return value


def filepath_validator(value: Path) -> Path:
    if is_valid_filepath(value, platform=sys.platform):
        return value
    else:
        sanitized_value = sanitize_filepath(value, platform=sys.platform)
        log.warning(
            f"Invalid filepath: {value}, automatically fix to {sanitized_value}"
        )
        return sanitized_value


def resolve_path(value: Path) -> Path:
    return value.resolve()


def path_exist_validator(value: Path) -> Path:
    if value.exists():
        return value
    raise ValueError(f"Path does not exist:{value}")


def not_none(v: Any) -> bool:
    return v is not None


def NDArrayValidator(shape, dtype):
    # See https://github.com/p2p-ld/numpydantic/issues/41
    return GetPydanticSchema(
        lambda tp, handler: NDArray.__get_pydantic_core_schema__(
            NDArray[shape, dtype], handler
        )
    )


# Jobs ##########################################
type ZeroToOneOpen = Annotated[float, Gt(0), Lt(1)]
type ZeroToOneClose = Annotated[float, Ge(0), Le(1)]
type Region = tuple[NonNegativeInt, NonNegativeInt, PositiveInt, PositiveInt]
type ColorImageArray = Annotated[
    np.ndarray, NDArrayValidator(Shape["* x, * y, 3 rgb"], np.uint8)  # type:ignore
]
type GrayImageArray = Annotated[
    np.ndarray, NDArrayValidator(Shape["* x, * y"], np.uint8)  # type:ignore
]
type ImageArray = ColorImageArray | GrayImageArray

# Path Management ###############################
# FileName ##################
type FileName = Annotated[NonEmptyStr, AfterValidator(filename_validator)]
type ImageFileName = Annotated[
    FileName,
    AfterValidator(lambda v: filename_extension_validator(v, IMAGE_EXTENSIONS)),
]
type JsonFileName = Annotated[
    FileName,
    AfterValidator(lambda v: filename_extension_validator(v, (".json", ".JSON"))),
]
type IniFileName = Annotated[
    FileName,
    AfterValidator(lambda v: filename_extension_validator(v, (".ini", ".INI"))),
]

# Path ######################
type FilePath = Annotated[
    Path, AfterValidator(filepath_validator), AfterValidator(resolve_path)
]
type ImagePath = Annotated[
    FilePath,
    AfterValidator(lambda v: filename_extension_validator(v, IMAGE_EXTENSIONS)),
]
type TxtPath = Annotated[
    FilePath,
    AfterValidator(lambda v: filename_extension_validator(v, (".txt", ".TXT"))),
]
type JsonPath = Annotated[
    FilePath,
    AfterValidator(lambda v: filename_extension_validator(v, (".json", ".JSON"))),
]
type IniPath = Annotated[
    FilePath,
    AfterValidator(lambda v: filename_extension_validator(v, (".ini", ".INI"))),
]

# Directory #################
type Directory = Annotated[
    Path, AfterValidator(filepath_validator), AfterValidator(resolve_path)
]
type DirectoryExisting = Annotated[Directory, AfterValidator(path_exist_validator)]


###########################################################
# Pydantic Model
###########################################################
class AlwaysValidateModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,  # IMPORTANT!!!, Check validator when change settings
        validate_default=True,  # validate default value
    )

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self._no_validate = False

    def no_validation_setter(
        self, name: str, value: Any, notice_observer: bool = True
    ) -> None:
        """
        临时禁用验证，直接设置模型字段
        用于通过property同时设置多个字段的场景，手动进行模型验证
        以避免多次验证的开销，以及涉及多字段验证的同步问题
        """
        self.__dict__[name] = value  # pyright:ignore [reportIndexIssue]
        self.__pydantic_fields_set__.add(name)
        if notice_observer and isinstance(self, OnValueChangeModel):
            self.call_oberser_handlers(name, value)

    @contextlib.contextmanager
    def delay_validate(self, notice_observer: bool = True):
        self._no_validate = True
        try:
            yield
        finally:
            self._no_validate = False
            self.model_validate(self)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Pydantic's validator when working on 'After' mode,
        even it cause a ValidationError, the attribute will still be assigned.
        AlwaysValidateModel save the previous status to roll back.
        """
        if hasattr(self, "_no_validate") and getattr(self, "_no_validate"):
            self.no_validation_setter(name, value, True)
            return
        _old_value = (
            deepcopy(self.__getattribute__(name)) if hasattr(self, name) else None
        )
        try:
            super().__setattr__(name, value)
        except ValidationError as e:
            # log.error(e)
            if _old_value is not None:
                super().__setattr__(name, _old_value)
            raise e  # pass to outside logic


class OnValueChangeModel(BaseModel):
    __hash__: Callable = (
        object.__hash__
    )  # add hash func to allow model be added to a dict

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self._observer_handler: dict[str, list[Callable[[Any], None]]] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        """Set pydantic field name to attribute object"""
        super().__setattr__(name, value)
        self.call_oberser_handlers(name, value)

    def setattr_block_observer(self, name: str, value: Any) -> None:
        """setattr with no handler call"""
        super().__setattr__(name, value)

    def call_oberser_handlers(self, field_name: str, value: Any | None = None):
        if value is None:
            value = self.__getattribute__(field_name)
        if field_name in self._observer_handler.keys():
            [f(value) for f in self._observer_handler[field_name]]

    def add_observer_handler(self, field_name: str, func: Callable[[Any], None]):
        if not hasattr(self, field_name):
            raise ValueError(f"{field_name} not in model_fields")
        if not self._observer_handler.get(field_name):
            self._observer_handler[field_name] = []
        self._observer_handler[field_name].append(func)

    def add_observer_handlers(
        self, field_names: list[str], func: Callable[[Any], None]
    ):
        for name in field_names:
            self.add_observer_handler(name, func)

    def remove_observer_handler(self, field_name: str, func: Callable[[Any], None]):
        if not hasattr(self, field_name):
            raise ValueError(f"{field_name} not in model_fields")
        if (not self._observer_handler.get(field_name)) or (
            func not in self._observer_handler[field_name]
        ):
            raise ValueError(f"func not in {field_name}`s observer handlers")
        self._observer_handler[field_name].remove(func)

    def remove_observer_handlers(
        self, field_names: list[str], func: Callable[[Any], None]
    ):
        for name in field_names:
            self.remove_observer_handler(name, func)

    def notice_model_observers(self) -> None:
        for name in self.__class__.model_fields.keys():
            if funcs := self._observer_handler.get(name):
                [f(getattr(self, name)) for f in funcs]


###########################################################
# Other types
###########################################################
class Flag:
    """Flag for threading status and jump out"""

    def __init__(self, value: bool) -> None:
        self._value = bool(value)
        self._lock = threading.RLock()

    @property
    def value(self) -> bool:
        with self._lock:
            return self._value

    @value.setter
    def value(self, v) -> None:
        with self._lock:
            self._value = bool(v)

    def __bool__(self) -> bool:
        """For 'if flag:' usage"""
        with self._lock:
            return self._value

    def set(self, value: bool) -> None:
        with self._lock:
            self._value = bool(value)

    def toggle(self) -> None:
        with self._lock:
            self._value = not self._value


class Line(AlwaysValidateModel):
    """线段类型，存储起始线段的坐标，以及在对应方向上的厚度"""

    direction: Direction
    image_shape: tuple[PositiveInt, PositiveInt]  # array shape, (height, width)
    point1: tuple[NonNegativeInt, NonNegativeInt]  # (x,y)
    point2: tuple[NonNegativeInt, NonNegativeInt]
    thickness: PositiveInt

    @property
    def start_index(self) -> int:
        return self.point1[self.normal_direction]

    @property
    def end_index(self) -> int:
        return self.point1[self.normal_direction] + self.thickness - 1

    @property
    def normal_direction(self) -> int:
        # as the reference index of point tuple
        if self.direction == Direction.HORIZONTAL:
            return 1
        elif self.direction == Direction.VERTICAL:
            return 0
        else:
            raise ValueError(f"Invalid direction {self.direction}")

    @model_validator(mode="after")
    def line_validator(self):
        not_normal_direction = int(not self.normal_direction)
        if self.point1[self.normal_direction] != self.point2[self.normal_direction]:
            raise ValueError("Only support horizontal and vertical lines")
        if self.point1[not_normal_direction] == self.point2[not_normal_direction]:
            raise ValueError("Point1 and Point2 can not be the same point")
        if (
            self.point1[0] >= self.image_shape[1]
            or self.point1[1] >= self.image_shape[0]
        ):
            raise ValueError("Line point1 out off the image bounds")
        if (
            self.point2[0] >= self.image_shape[1]
            or self.point2[1] >= self.image_shape[0]
        ):
            raise ValueError("Line point2 out off the image bounds")
        if self.end_index >= self.image_shape[not_normal_direction]:
            raise ValueError("Line out off the image bounds because it's too thick!!!")
        return self

    def draw(self, img: np.ndarray | cv2.Mat, color: Color = Color("#00FF00")) -> None:
        """
        绘制线段到输入图像
        :param img: 要绘制的原始图像
        :param color: 绘制颜色，color类型，默认值为绿色
        """
        bgr_color = self.color2bgr(color)
        p1 = list(self.point1)
        p2 = list(self.point2)
        for _ in range(self.thickness):
            cv2.line(img, p1, p2, bgr_color, thickness=1)
            p1[self.normal_direction] += 1
            p2[self.normal_direction] += 1

    def get_index_points(
        self, extern_width: int = 0, reverse: bool = False
    ) -> np.ndarray:
        """获取线段在相应方向上的索引值，并相周围扩展额外的像素值"""
        p1 = list(self.point1)
        p1[self.normal_direction] -= (
            extern_width if p1[self.normal_direction] >= extern_width else 0
        )  # 避免出现负数
        thickness = self.thickness + extern_width * 2

        index_points = np.arange(
            p1[self.normal_direction], p1[self.normal_direction] + thickness
        )
        edge = (
            self.image_shape[0]
            if self.direction == Direction.HORIZONTAL
            else self.image_shape[1]
        )
        index_points = np.delete(index_points, np.argwhere(index_points >= edge))

        if reverse:
            index_points = edge - index_points  # 翻转索引值正方向
        return index_points

    def move_right(
        self, pixel: int, image_shape: Optional[tuple[int, int]] = None
    ) -> None:
        """将线段延水平方向移动指定像素，向右为正"""
        p1, p2 = list(self.point1), list(self.point2)
        p1[0] += pixel
        p2[0] += pixel
        try:
            new_line = Line(
                point1=(p1[0], p1[1]),
                point2=(p2[0], p2[1]),
                thickness=self.thickness,
                direction=self.direction,
                image_shape=image_shape
                if image_shape is not None
                else self.image_shape,
            )
        except ValidationError as e:
            log.warning(e)
            return
        else:
            self.__init__(**new_line.model_dump())

    @staticmethod
    def color2bgr(color: Color) -> tuple[int, int, int]:
        rgb_color = color.__getattribute__("_rgba")
        return (int(rgb_color.b * 255), int(rgb_color.g * 255), int(rgb_color.r * 255))


class RegionData(AlwaysValidateModel, OnValueChangeModel):
    monitor_num: PositiveInt = 1
    x: Annotated[NonNegativeInt, AfterValidator(lambda v: int(v))]
    y: Annotated[NonNegativeInt, AfterValidator(lambda v: int(v))]
    width: Annotated[PositiveInt, AfterValidator(lambda v: int(v))]
    height: Annotated[PositiveInt, AfterValidator(lambda v: int(v))]

    def __init__(
        self,
        x: NonNegativeInt | None = None,
        y: NonNegativeInt | None = None,
        width: PositiveInt | None = None,
        height: PositiveInt | None = None,
        monitor_num: PositiveInt = 1,
        region: Region | None = None,
    ):
        if all(map(not_none, [x, y, width, height])):
            super().__init__(
                x=x, y=y, width=width, height=height, monitor_num=monitor_num
            )
            return
        elif region:
            super().__init__(
                x=region[0],
                y=region[1],
                width=region[2],
                height=region[3],
                monitor_num=monitor_num,
            )
            return
        else:
            raise ValueError("Invaild RegionData paremeter")

    @property
    def region(self) -> Region:
        return (self.x, self.y, self.width, self.height)

    @region.setter
    def region(self, value: Region):
        with self.delay_validate():
            self.x, self.y, self.width, self.height = value

    @model_validator(mode="after")
    def validate_region(self) -> Self:
        with mss.mss() as sct:
            monitors = sct.monitors
            if self.monitor_num < 1 or self.monitor_num > len(monitors) - 1:
                raise ValueError(f"Invalid monitor_num:{self.monitor_num}")
            monitor = monitors[self.monitor_num]
            if (
                self.x < 0
                or self.y < 0
                or self.x + self.width > monitor["width"]
                or self.y + self.height > monitor["height"]
            ):
                raise ValueError(
                    f"Region-{self.region} out off num-({self.monitor_num}) screen bounds: {monitor}"
                )
        return self


class Singleton:
    """MultiThread Safe Singleton class Decorator"""

    _instances: dict[type, object] = {}
    _lock = threading.RLock()

    def __init__(self, cls: type):
        self._cls = cls
        self.__name__ = cls.__name__
        self.__module__ = cls.__module__
        self.__doc__ = cls.__doc__

    def __call__(self, *args, **kwargs):
        cls = self._cls
        if cls not in self._instances:
            with self._lock:
                if cls not in self._instances:
                    self._instances[cls] = cls(*args, **kwargs)
        return self._instances[cls]

    def __instancecheck__(self, instance):
        return isinstance(instance, self._cls)

    def __subclasscheck__(self, subclass):
        return issubclass(subclass, self._cls)
