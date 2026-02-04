import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Self

from loguru import logger as log
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    ValidationError,
    model_validator,
    validate_call,
)
from pydantic_extra_types.color import Color
from PySide6.QtCore import Qt

from src.Model.Data.const import (
    Align,
    CaptureTool,
    Direction,
    ImageCompareMethod,
    ImageSavingFormat,
    LogLevel,
    PreviewLines,
    ReclipMethod,
    StitchMethod,
)
from src.Model.Data.type import (
    AlwaysValidateModel,
    Directory,
    DirectoryExisting,
    FileName,
    JsonFileName,
    NonEmptyStr,
    OnValueChangeModel,
    RegionData,
    TxtPath,
    ZeroToOneOpen,
)


###########################################################
# Field default factories
###########################################################
def default_tool_factory() -> CaptureTool:
    if os.environ.get("XDG_SESSION_TYPE") == "wayland":
        if os.environ.get("XDG_SESSION_DESKTOP") == "KDE":
            return CaptureTool.SPECTACLE
        # 使用command -v检查命令是否存在
        elif subprocess.run(
            ["command -v grim"], shell=True, capture_output=True
        ).stdout:
            return CaptureTool.GRIM
    return CaptureTool.MSS


def get_exec_main_dir() -> DirectoryExisting:
    if getattr(sys, "frozen", False):  # 检测程序是否处于编译环境
        return Path(sys.argv[0]).resolve().parent  # 当编译后运行时，返回exe文件的路径
    else:
        return Path(sys.argv[0]).resolve().parent  # 脚本运行时


###########################################################
# App Settings
# as well as the app status
###########################################################
class SettingsModel(AlwaysValidateModel, OnValueChangeModel):
    model_config = ConfigDict(extra="forbid")  # Do Not allow extra parameter

    # TODO 序列化
    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)


class LocateSettings(SettingsModel):
    locate_offset: tuple[int, int, int, int] = Field(default=(0, 0, 0, 0))
    window_opacity: ZeroToOneOpen = 0.4
    window_always_on_top: bool = False
    window_auto_close: bool = False
    window_limit_move: bool = True
    live_locate: bool = False
    region_data: RegionData = RegionData(0, 0, 514, 114, 1)


class CaptureSettings(SettingsModel):
    tool: CaptureTool = Field(default_factory=default_tool_factory)
    save_format: ImageSavingFormat = ImageSavingFormat.JPEG
    delay_time: PositiveFloat = 0.7  # seconds
    if_keep_last: bool = True
    if_reverse_image: bool = False
    capture_data_filename: JsonFileName = "CaptureData.json"


class BuildImageSettings(SettingsModel):
    compare_method: ImageCompareMethod = ImageCompareMethod.SSIM
    compare_threshold: PositiveFloat = 0.96

    @model_validator(mode="after")
    def validate_compare_threshold(self) -> Self:
        if self.compare_method == ImageCompareMethod.SSIM:
            if 0 < self.compare_threshold < 1:
                return self
            raise ValueError("compare_threshold must between 0-1 when using SSIM")
        elif self.compare_method == ImageCompareMethod.MSE:
            if 0 < self.compare_threshold < 65025:
                return self
            raise ValueError("compare_threshold must between 0-65025 when using MSE")
        else:
            raise ValueError(f"Invalid compare_method {self.compare_method}")


class StitchSettings(SettingsModel):
    method: StitchMethod = StitchMethod.MSE
    direction: Direction = Direction.HORIZONTAL
    saving_format: ImageSavingFormat = ImageSavingFormat.JPEG
    ui_lock_zoom: bool = False
    add_mark_point: bool = True
    location_mark_point: ZeroToOneOpen = 0.35


class ReclipSettings(SettingsModel):
    method: ReclipMethod = ReclipMethod.FIXED_BAR_NUM
    bar_num_each_line: PositiveInt = 4
    bar_num_line_max_length: PositiveInt = 4
    clip_align: Align = Align.LEFT
    clip_margin: NonNegativeInt = 4
    clip_resize: bool = True
    clip_resize_threshold: ZeroToOneOpen = 0.5
    saving_format: ImageSavingFormat = ImageSavingFormat.JPEG
    live_preview: bool = False
    font_name: str = ""


class ScoreStyleSettings(SettingsModel):
    title: NonEmptyStr = "untitled"


class LogSettings(SettingsModel):
    class LogColorConfig(SettingsModel):
        debug: Color = Color("grey")
        info: Color = Color("black")
        success: Color = Color("green")
        warning: Color = Color("orange")
        error: Color = Color("red")

    log_path: TxtPath = Field(
        default_factory=lambda: get_exec_main_dir() / "logs" / "main_log.txt"
    )
    log_main_rotation: str = "1MB"  # When to create a new log file
    log_main_retention: str | int = 5  # When delete old log file
    save_level: LogLevel = LogLevel.DEBUG
    save_format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> "
        "| Thread:{thread} | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>"
    )
    show_level: LogLevel = LogLevel.DEBUG
    show_format: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> "
        "| <level>{message}</level>"
    )
    color_config: LogColorConfig = LogColorConfig()
    auto_scroll: bool = True


class LineDetectorSettings(SettingsModel):
    coefficient_horizontal: PositiveFloat = 0.7
    coefficient_vertical: PositiveFloat = 0.8


class PathSettings(SettingsModel):
    exe_dir: DirectoryExisting = Field(default_factory=get_exec_main_dir)
    main_out_dir: Directory = Field(
        default_factory=lambda: get_exec_main_dir() / "output"
    )
    score_title: FileName = "untitled"

    @property
    def config_dir(self) -> Directory:
        return self.exe_dir / "config"

    @property
    def working_dir(self) -> Directory:
        return self.main_out_dir / self.score_title

    @working_dir.setter
    def working_dir(self, value: Directory):
        self.main_out_dir = value.parent
        self.score_title = value.name


class ConfigSettings(SettingsModel):
    auto_save_all: bool = True


class ShortcutSettings(SettingsModel):
    manualStitch_key_min_index: int = Qt.Key.Key_PageUp
    manualStitch_key_max_index: int = Qt.Key.Key_PageDown
    manualStitch_key_prev_index: int = Qt.Key.Key_Up
    manualStitch_key_next_index: int = Qt.Key.Key_Down
    manualStitch_key_max_point: int = Qt.Key.Key_Home
    manualStitch_key_min_point: int = Qt.Key.Key_End
    manualStitch_key_add_point: int = Qt.Key.Key_Left
    manualStitch_key_sub_point: int = Qt.Key.Key_Right
    manualStitch_point_step_normal: PositiveInt = 1
    manualStitch_point_step_shift: PositiveInt = 20
    manualStitch_point_step_ctrl: PositiveInt = 50
    manualStitch_point_step_cs: PositiveInt = 200
    manualStitch_index_step_normal: PositiveInt = 1
    manualStitch_index_step_shift: PositiveInt = 5
    manualStitch_index_step_ctrl: PositiveInt = 10
    manualStitch_index_step_cs: PositiveInt = 20
    _key_shift_with_ctrl = (
        Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier
    )

    def get_move_step(
        self, type: Literal["index", "point"], modifier: Qt.KeyboardModifier
    ) -> PositiveInt:
        match modifier:
            case Qt.KeyboardModifier.ShiftModifier:
                if type == "index":
                    return self.manualStitch_index_step_shift
                elif type == "point":
                    return self.manualStitch_point_step_shift
            case Qt.KeyboardModifier.ControlModifier:
                if type == "index":
                    return self.manualStitch_index_step_ctrl
                elif type == "point":
                    return self.manualStitch_point_step_ctrl
            case self._key_shift_with_ctrl:
                if type == "index":
                    return self.manualStitch_index_step_cs
                elif type == "point":
                    return self.manualStitch_point_step_cs
            case _:
                if type == "index":
                    return self.manualStitch_index_step_normal
                elif type == "point":
                    return self.manualStitch_point_step_normal


class GUISettings(SettingsModel):
    mainWindow_always_on_top: bool = True
    mainWindow_dock_perspective: str = "default"
    imageViewer_show_tools: bool = False


class PreviewSettings(SettingsModel):
    preview_lines: PreviewLines = PreviewLines.ALL
    live_preview: bool = False
    live_detect: bool = False
    save_preview: bool = False


class AppSettings(SettingsModel):
    gui_settings: GUISettings = GUISettings()
    path_settings: PathSettings = PathSettings()
    log_settings: LogSettings = LogSettings()
    config_settings: ConfigSettings = ConfigSettings()
    locate_settings: LocateSettings = LocateSettings()
    preview_settings: PreviewSettings = PreviewSettings()
    capture_settings: CaptureSettings = CaptureSettings()
    build_image_settings: BuildImageSettings = BuildImageSettings()
    stitch_settings: StitchSettings = StitchSettings()
    recip_settings: ReclipSettings = ReclipSettings()
    line_detector_settings: LineDetectorSettings = LineDetectorSettings()

    def notice_all_observers(self) -> None:
        for model_name in self.__class__.model_fields.keys():
            model: OnValueChangeModel = getattr(self, model_name)
            model.notice_model_observers()

    def save(self) -> None:
        if not pathSettings.config_dir.exists():
            pathSettings.config_dir.mkdir()

        def update_dict(now: dict, old: dict, config: dict):
            for k in now.keys():
                if isinstance(now[k], dict):
                    update_dict(now[k], old.get(k, {}), config.get(k, {}))
                elif k in old.keys() and not config.get(k, False):
                    now[k] = old[k]  # update to old value (not saving)

        now_dict = self.model_dump()

        if not self.config_settings.auto_save_all:
            old_dict = self.load().model_dump()
            config_dict = appSettingsSavingConfig
            update_dict(now_dict, old_dict, config_dict)

        try:
            with open(
                file=self.path_settings.config_dir / "AppSettings.json",
                mode="w",
                encoding="utf-8",
            ) as f:
                f.write(AppSettings.model_validate(now_dict).model_dump_json(indent=4))
        except ValidationError as e:
            log.warning(f"AppSettings Saving Failed: {e}")

    def load(self) -> "AppSettings":
        """Load settings for config dir, return a updated new model"""
        new_model = self.model_copy(deep=True)
        try:
            file_path = self.path_settings.config_dir / "AppSettings.json"
            with open(file=file_path, mode="r", encoding="utf-8") as f:
                local_json = json.load(f)
                if not isinstance(local_json, dict):
                    log.warning("AppSettings load failed, settings json must be a dict")
                    return self
                update_json_to_model(local_json, new_model)
            return new_model
        except FileNotFoundError:
            log.warning(f"AppSettings load failed, {file_path} Not Found")
            return self


@validate_call
def update_json_to_model(json: dict, model: BaseModel):
    field_names = list(model.__class__.model_fields.keys())
    for k, v in json.items():
        if k in field_names:
            if isinstance(v, dict) and isinstance(
                submodel := getattr(model, k), BaseModel
            ):
                update_json_to_model(v, submodel)
                continue
            try:
                setattr(model, k, v)
            except ValidationError as e:
                log.debug(e)
                log.warning(
                    f"Invalid field_value:{v} for {k} when loading {model.__class__.__name__} from json"
                )
        else:
            log.warning(
                f"Invalid field_name:{k} when loading {model.__class__.__name__} from json"
            )


class AppSettingsSavingConfig(dict):
    def __init__(self, appSettings: AppSettings = AppSettings(), d: dict | None = None):
        if d is not None:
            super().__init__(d)
            return
        super().__init__(appSettings.model_dump())

        def set_value(d: dict, value):
            for k, v in d.items():
                if isinstance(v, dict):
                    set_value(v, value)
                    continue
                else:
                    d[k] = value

        set_value(self, True)

    @property
    def json(self) -> str:
        return json.dumps(self, indent=4)

    def save(self) -> None:
        if not pathSettings.config_dir.exists():
            pathSettings.config_dir.mkdir()
        with open(
            pathSettings.config_dir / "AppSettingsSavingConfig.json",
            mode="w",
            encoding="utf-8",
        ) as f:
            f.write(self.json)

    def load(self) -> "AppSettingsSavingConfig":
        try:
            file_path = pathSettings.config_dir / "AppSettingsSavingConfig.json"
            with open(file_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return AppSettingsSavingConfig(d=config)
        except ValidationError:
            log.warning(
                "AppSettingsSavingConfig load failed, using defalut config with all true"
            )
        except FileNotFoundError:
            log.info(f"{file_path} Not Found, using default config")
        return self


appSettings = AppSettings().load()
guiSettings = appSettings.gui_settings
pathSettings = appSettings.path_settings
logSettings = appSettings.log_settings
configSettings = appSettings.config_settings
locateSettings = appSettings.locate_settings
previewSettings = appSettings.preview_settings
captureSettings = appSettings.capture_settings
buildImageSettings = appSettings.build_image_settings
stitchSettings = appSettings.stitch_settings
reclipSettings = appSettings.recip_settings
lineDetectorSettings = appSettings.line_detector_settings
log.info("AppSettings load complete")

appSettingsSavingConfig = AppSettingsSavingConfig().load()
log.info("AppSettingsSavingConfig load complete")
