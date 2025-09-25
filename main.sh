#!/bin/bash
###########################################################
# The main entry point of the application
# It sets up the environment and starts the Qt application
###########################################################

source .venv/bin/activate

# solve fcitx input method issue on linux
pyside_path=$(python -c "import PySide6; print(PySide6.__path__[0])")
export LD_LIBRARY_PATH="${pyside_path}/Qt/lib:${LD_LIBRARY_PATH}"
export QT_PLUGIN_PATH="${pyside_path}/Qt/plugins:${QT_PLUGIN_PATH}"

# solve the windows position issue on linux wayland
export QT_QPA_PLATFORM="xcb"

python src/main.py
