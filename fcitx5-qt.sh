#!/bin/bash
###########################################################
# This script install and build fcitx5-qt plugin for Pyside
# You may need to install extra-cmake-modules 
#     or libfcitx5utils-dev using your package manager
###########################################################
source .venv/bin/activate
pyside_path=$(python -c "import PySide6; print(PySide6.__path__[0])")

git clone https://github.com/fcitx/fcitx5-qt.git
cd fcitx5-qt
export LD_LIBRARY_PATH="${pyside_path}/Qt/lib"
cmake -DCMAKE_PREFIX_PATH=${pyside_path}/Qt -DENABLE_QT4=OFF -DENABLE_QT5=OFF -DENABLE_QT6=ON -DBUILD_ONLY_PLUGIN=ON -DBUILD_STATIC_PLUGIN=OFF -DWITH_FCITX_PLUGIN_NAME=ON -B build .
cd build
make -j ${nproc}
cp ${PWD}/qt6/platforminputcontext/libfcitx5platforminputcontextplugin.so ${pyside_path}/Qt/plugins/platforminputcontexts/

cd .. && cd ..
rm -rf fcitx5-qt
