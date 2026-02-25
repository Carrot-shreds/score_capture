from enum import IntEnum, StrEnum

###########################################################
# Constant Num
###########################################################
MAIN_WINDOW_SIZE: tuple[int, int] = (800, 500)  # width, height
IMAGE_EXTENSIONS: tuple[str, ...] = (
    ".jpg",
    ".jpeg",
    ".png",
)


###########################################################
# Enum definition
###########################################################
class ImageCompareMethod(StrEnum):
    SSIM = "SSIM"
    MSE = "MSE"


class DetectMethod(StrEnum):
    SSIM = "SSIM"
    MSE = "MSE"


class StitchMethod(StrEnum):
    DIRECT = "DIRECT"
    SSIM = "SSIM"
    MSE = "MSE"


class PreviewLines(IntEnum):
    ONLY_V = 0
    ONLY_H = 1
    ALL = 2


class ReclipMethod(IntEnum):
    FIXED_BAR_NUM = 0
    FILL_MAX_WIDTH = 1


class Align(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Direction(IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1

    @property
    def reverse(self) -> "Direction":
        if self is Direction.HORIZONTAL:
            return Direction.VERTICAL
        else:
            return Direction.HORIZONTAL

    @property
    def str(self) -> str:
        if self is Direction.HORIZONTAL:
            return "horizontal"
        else:
            return "vertical"


class CaptureTool(StrEnum):
    MSS = "mss"
    SPECTACLE = "spectacle"
    GRIM = "grim"


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ImageSavingFormat(StrEnum):
    JPEG = ".jpg"
    PNG = ".png"
