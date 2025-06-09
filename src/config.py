from typing import Optional
import configparser
from configparser import ConfigParser

from loguru import logger as log

class Config:
    """
    配置文件管理类
    """

    def __init__(self, data):
        self.config_reader = ConfigParser()

        self.data = data
        self.image:dict[str, list] = {
            f"{self.data.if_auto_manage_config=}": [[bool], ["Config", "auto_manage_config"]],

            f"{self.data.log_output_level=}": [[str, ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR"]],
                                               ["Log", "log_output_level"]],

            f"{self.data.score_save_path=}": [[str], ["Saving", "saving_path"]],
            #f"{self.data.score_title=}": [[str], ["Saving", "score_title"]],
            f"{self.data.score_save_format=}": [[str, [".jpg", ".png"]], ["Saving", "score_saving_format"]],

            f"{self.data.compare_method=}": [[str, ["SSIM", "MSE"]], ["Capture", "compare_method"]],
            f"{self.data.compare_threshold=}": [[float], ["Capture", "compare_threshold"]],
            f"{self.data.capture_delay=}": [[float], ["Capture", "capture_delay"]],
            f"{self.data.if_keep_last=}": [[bool], ["Capture", "if_keep_last_group"]],
            f"{self.data.if_reverse_image=}": [[bool], ["Capture", "if_reverse_image"]],
        }
        self.image = {k.split("=")[0].split(".")[-1]: v for k, v in self.image.items()}  # 获取变量名作为Key

    def save_config_to_ini(self, ini_file: Optional[str] = None) -> None:
        """保存data中的配置项到ini文件"""
        if ini_file is None:
            ini_file = self.data.ini_file
        new_ini = ConfigParser()
        new_ini.add_section("Config")
        new_ini.add_section("Log")
        new_ini.add_section("Saving")
        new_ini.add_section("Capture")

        for key, value in self.image.items():
            new_ini.set(self.image[key][1][0], self.image[key][1][1],
                        str(self.data.__dict__[key]))
        with open(ini_file, "w") as f:
            f.truncate()  # 清空文件
            new_ini.write(f)
        log.info(f"成功将配置保存至{ini_file}")

    def read_data_from_ini(self, ini_file: Optional[str] = None) -> None:
        """从.ini文件中导入数据"""
        if ini_file is None:
            ini_file = self.data.ini_file

        try:
            if not self.config_reader.read(ini_file):
                return log.error(f"读取配置文件{ini_file}错误,检查配置文件位置")
        except configparser.Error:
            return log.error(f"读取配置文件{ini_file}错误,请检查文件格式")
        if not self.check_config():
            return log.warning("未成功读取配置文件")

        for key, value in self.image.items():
            self.data.__dict__[key] = self.transform_data(self.config_reader[value[1][0]][value[1][1]], value[0])
        return log.info(f"成功读取配置文件{ini_file}")

    def check_config(self) -> bool:
        """检查配置文件格式和数据"""
        for key, value in self.image.items():
            try:
                self.transform_data(self.config_reader[value[1][0]][value[1][1]], value[0])
            except ValueError:
                return False
            except KeyError:
                return False
        return True

    def transform_data(self, data: str, args: list) -> bool | str | int | float:
        """根据类型转换data，有问题则抛出TypeError"""
        if len(args) == 2:
            func_args = args[1]
        else:
            func_args = []

        match args[0]:
            case bool():
                return self.str_to_bool(data)
            case float():
                return self.str_to_digit(data)
            case str():
                if func_args:
                    return self.if_str_in_range(data, func_args)
                else:
                    return data
            case _:
                return data


    @staticmethod
    def str_to_bool(string: str) -> bool:
        """将文字转化为bool"""
        if string == "true" or string == "True":
            return True
        elif string == "false" or string == "False":
            return False
        else:
            log.error("配置文件错误，请检查ini中的bool值拼写")
            raise ValueError

    @staticmethod
    def if_str_in_range(string: str, str_range: list[str]) -> str:
        """检查字符串是否在指定范围内"""
        if string in str_range:
            return string
        else:
            log.error(f"配置文件错误，值{string}非法，应为{str_range}")
            raise ValueError

    @staticmethod
    def str_to_digit(string: str) -> float | int:
        """检查是否为数字"""
        if string.isdigit():
            return int(string)
        else:
            s = string.split(".")
            if len(s) == 2 and s[0].isdigit() and s[1].isdigit():
                return float(string)
            else:
                log.error("配置文件错误，值{string}非法，应为数字")
                raise ValueError


