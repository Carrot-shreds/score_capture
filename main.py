# This program is free software:you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.

import sys

from loguru import logger as log

from src import __version__


def show_main_window() -> None:
    from PySide6 import QtCore
    from PySide6.QtWidgets import QApplication

    # init qfile resource during import
    from src.resource import compiled_resource  # noqa:F401
    from src.ViewModel.MainWindow import MainWindow_VM

    """主窗口进程函数"""
    # dps缩放设定，详见https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.Qt.HighDpiScaleFactorRoundingPolicy
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )  # default

    # Ignore Error - "qt.qpa.window: SetProcessDpiAwarenessContext() failed"
    QtCore.QLoggingCategory.setFilterRules("qt.qpa.window.warning=false")
    app = QApplication(sys.argv)
    window = MainWindow_VM()
    window.show()
    window.activateWindow()
    app.exec()


def init_log() -> None:
    """init logmanager and detour log output"""
    from src.Model.Data.settings import logSettings
    from src.Model.log import logManager

    logManager.init_log_settings(logSettings)


def load_config() -> None:
    from src.Model.Data.settings import (
        appSettingsSavingConfig,
        load_all_settings,
    )

    load_all_settings()
    appSettingsSavingConfig = appSettingsSavingConfig.load()
    init_log()  # update logSettings for logmanager


def main() -> None:
    init_log()  # init log detour
    log.debug("=====Main_starting=====")
    log.debug(f"Current version: {__version__}")
    load_config()
    show_main_window()
    log.debug("=====Main_finished=====")


if __name__ == "__main__":
    main()
