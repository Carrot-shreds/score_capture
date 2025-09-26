# Score Capture

Capture, Detect, Stitch and Reclip score/TAB
from online video to generate printable image.

Work In Progress

## 从源码运行/开发

下载解压源码zip，或使用git clone到本地

    git clone https://github.com/Carrot-shreds/score_capture.git

切换到项目根目录

    cd score_capture

安装uv环境

    pip install uv 或
    wget -qO- https://astral.sh/uv/install.sh | sh

同步构建环境

    uv sync

运行程序入口

    uv run ./src/main.py
    (Linux) bash main.sh

获取更新

    git pull

从源码构建exe编译

    uv run ./build.py
