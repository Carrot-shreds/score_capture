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
from PySide6.QtGui import QPixmap

from src import __version__


def show_main_window() -> None:
    import os

    import pyqtgraph
    from PySide6 import QtAsyncio, QtCore
    from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
    from PySide6.QtWidgets import QApplication

    from src.Model.Data.settings import guiSettings

    # init qfile resource during import
    from src.resource import compiled_resource  # noqa:F401
    from src.ViewModel.MainWindow import MainWindow_VM

    pyqtgraph.setConfigOption("useNumba", True)  # Speed up for image render.

    # dpi scale setting，Reference: https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html#PySide6.QtCore.Qt.HighDpiScaleFactorRoundingPolicy
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )  # default
    os.environ["QT_SCALE_FACTOR"] = str(guiSettings.ui_scaling)
    log.debug(f"Ui Scaling: {guiSettings.ui_scaling}")

    # Ignore Error - "qt.qpa.window: SetProcessDpiAwarenessContext() failed"
    QtCore.QLoggingCategory.setFilterRules("qt.qpa.window.warning=false")
    app = QApplication(sys.argv)
    try:
        from ctypes import windll  # Only exists on Windows.

        appid = f"Carrot-shreds.score_capture.{__version__}"
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
    except ImportError:
        pass
    app.setWindowIcon(QPixmap(":/icon"))

    # Load language files
    path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    translator = QTranslator(app)
    if (
        translator.load(QLocale.system(), "qtbase", "_", path)
        if (lang := guiSettings.language) == ""
        else translator.load("qtbase_" + lang, path)
    ):
        app.installTranslator(translator)
    translator = QTranslator(app)
    translation_path = ":/translations"
    if (
        translator.load(QLocale.system(), "", "", translation_path)
        if (lang := guiSettings.language) == ""
        else translator.load(lang, translation_path)
    ):
        app.installTranslator(translator)
        if (lang := translator.language()) != guiSettings.language:
            guiSettings.language = lang
        log.debug(f"Loaded Language: {lang}")
    else:
        log.debug("Loaded Language: en (defult)")

    window = MainWindow_VM()
    window.show()
    window.activateWindow()
    QtAsyncio.run()  # Replace app.exec() to support asyncio


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
    log.debug("=====Main Starting=====")
    log.debug(("Current version: {}").format(__version__))
    load_config()
    show_main_window()
    log.debug("=====Main Finished=====")


if __name__ == "__main__":
    main()
