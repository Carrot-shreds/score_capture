# Score Capture

![GitHub Tag](https://img.shields.io/github/v/tag/carrot-shreds/score_capture)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FCarrot-shreds%2Fscore_capture%2Fmaster%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/carrot-shreds/score_capture)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
![GitHub Repo stars](https://img.shields.io/github/stars/carrot-shreds/score_capture)

[简体中文](README.md)  [English](/docs/README_en.md)

从滚动视频乐谱中，截取、识别、拼接并重分割，格式化生成可打印的曲谱图像。

<details>
    <summary>界面截图</summary>
    <img src="/docs/screenshot/Preview_zh_CN.png" alt="Tab Preview">
    <img src="/docs/screenshot/Stitch_zh_CN.png" alt="Tab Stitch">
    <img src="/docs/screenshot/Reclip_zh_CN.png" alt="Tab Reclip">
    <img src="/docs/screenshot/Settings_zh_CN.png" alt="Tab Settings">
</details>

## 特性
- [x] 支持竖向或横向滚动的曲谱视频
- [x] 识别谱线并自动化拼接
- [x] 易用的手动拼接调整工具
- [x] 基础曲谱样式编辑
- [x] 支持MSS库或命令行工具实现跨平台截图
- [x] 基于窗口的动态预览定位
- [x] 响应式UI设置
- [x] 基于QtAds的Docking布局
- [ ] 直接从视频文件中提取图片
- [ ] 基于鼠标框选的定位系统
- [ ] 更加完善的跨平台支持
- [ ] 五线谱优化
- [ ] 多音轨支持

## i18n
- [x] English
- [x] 简体中文

## 安装 / 使用
<details>
    <summary>从源码运行 / 开发</summary>
    获取源码并进入项目根目录：

    git clone https://github.com/Carrot-shreds/score_capture.git
    cd score_capture

安装uv环境：

    curl -LsSf https://astral.sh/uv/install.sh | sh
    或
    pip install uv

同步构建环境（默认不包含开发依赖）：

    uv sync
    或
    uv sync --dev

编译Qt资源文件：

    uv run tools.py build

运行程序入口：

    uv run main.py
    (Linux) bash main.sh

获取仓库更新：

    git pull

从源码编译：

    uv run build.py
</details>

如果您使用Win10及以上的64位Windows系统，请下载最新 [release](https://github.com/Carrot-shreds/score_capture/releases/) 中的 `score_capture_xxx_win64.zip`。解压到合适的位置后，点击 `score_capture.exe` 即可启动。不需要进行额外的安装，所有配置和依赖都被打包到独立文件夹中，方便移动和卸载。  
对于MacOS和Linux用户，目前并不提供预编译版本，请自行参考上文中的说明，并尝试从源码运行。

## 文件命名约定
    # 图片
    capture：截图保存的单张原始图片，按设置可能经过反色处理
    image：对capture分组进行均值的图片，供后续使用
    detected：在原始图像上叠加了线段检测的结果
    stitched：对image拼接后的图片
    barlines：仅小节线识别的预览，用于重分割
    reclip：重分割后的横向拼接图片，或与竖直拼接图片相同
    # 数据文件(json)
    CaptureData：存储capture间的比较数据，用于重新生成image
    ScoreDetections：作为image的线段检测缓存，用于拼接
    StitchData：拼接点结果数据，可以从手动拼接窗口打开可视化编辑
    StyleData：存储最终生成图片的样式信息

## 配置文件
位于 `config` 文件夹中。

    AppSettings：存储了应用的绝大部分设置，可以手动编辑配置
    AppSettingsSavingConfig：AppSettings默认开启了始终保存所有设置，如果关闭的话，则只会保存在AppSettingsSavingConfig中设置为true的项。
    dockSettings：存储了当前所有的UI视图预设

建议经常保存配置文件的备份，以避免意外丢失或覆盖，只需要简单地复制一份config文件夹即可。

## 工作流程
> 图片文件名：capture[1-n] -> image[1-n] -> title-stitched -> title-recliped -> title[1-n]
0. 使用 `[主输出目录]//[文件夹标题]` 作为工作目录。
1. **（定位）** 通过定位窗口获取曲谱位置。
2. **（预览）** 通过预览窗口预览范围和线段识别参数（可选）。
3. **（截图）** 启动截图，播放视频，结束截图。在此过程中，每隔指定时间截图生成一张 `capture*.*` 图像。之后将两张以上“相同”（比较相似度）`capture`生成一张 `image*.*`。
4. **（识别）** 使用设置的参数对每张image进行线段识别，生成 `image-detected` 以及 `ScoreDetections.json`，主要需要使用小节线（即竖直线）的位置作为拼接时的参考。
5. **（拼接）** 以各小节线前后的范围为参考，拼接相邻的image，比较获得两张图像重叠最“完美”（最相似）的位置，保存到 `ScoreStitchData.json`，并拼接生成 `title-stitched`。
6. **（重分割）** 对 `title-stitched` 进行线段检测，生成 `title-stitched-detected` 与 `title-stitched-barlines`，主要也是获得拼接图中的小节线，用来将横向的长图从小节线前后切开，重新排版到竖向，生成 `title-reclip`。
7. 如果stitched图像本身就是竖向拼接的，那么则会额外检测反转的水平线，也就是两整行曲谱间的空白部分，以避免切分时将单行分开，保存预览到 `title-blank-gaps` 图像。
8. **（样式编辑）** 对 `title-reclip` 按打印比例切分，添加边距/标题/页码等样式，最终生成 `title*.*`，或保存到PDF。

## 快捷键
    # 主界面
    Ctrl 1-9：切换界面预设序号
    F12：切换窗口置顶状态
    F1-F5：主操作工具栏
    # 文件
    Ctrl-o：打开一个文件夹作为工作文件夹
    Ctrl-r：重命名当前文件夹
    Ctrl-p：打印当前的曲谱结果
    # 定位
    鼠标左键双击：切换显示模式
    鼠标右键双击：最小化窗口
    F12：切换窗口置顶状态
    # 手动拼接页面
    上下方向键：切换拼接点
    左右方向键：调整当前拼接点数值
    方向键 + Ctrl/Shift：不同的调整步长
    PageUp/PageDown：最小/最大拼接点数值
    Home/End：最小/最大拼接序号
    Ctrl+s：保存拼接数据和结果图片

## FAQ
### Score Capture 是跨平台的吗？
是的！本项目基于 Python 与 PySide（Qt 的 Python 绑定），设计上能够支持 Windows / MacOS / Linux 系统桌面端跨平台。但是目前除 Windows 外的测试仍然比较欠缺，可能会存在一定的兼容性问题。
### 为什么 Win7 系统无法运行？
Python 官方在 3.9 版本之后放弃了对 Win7 的支持，需要依赖额外的社区移植，暂时并没有这个计划。
### 为什么我的 fcitx 输入法打不出字？
在 Linux 上运行时请使用 `bash main.sh` 启动主程序，以确保加载 libfcitx5 插件。如果预编译插件加载失败，尝试使用 `bash fcitx5-qt.sh` 重新编译。
### 它支持 xxx 类型的曲谱吗？
考虑到曲谱类型的多样，以及视频质量的不同，开发测试通常无法覆盖全部情况。开发将会优先考虑 **横向滚动的 TAB 曲谱**，而关于纵向滚动、五线谱等其他类型的支持，则需要通过更多的用户测试与反馈进行改善。如果遇到了问题，请尝试使用手动拼接工具，或是将其作为一个 issue 进行反馈。

## 贡献
本项目仍在持续开发当中，欢迎各种形式的贡献，包括但不限于：
- 报告漏洞
- 新功能建议
- 跨平台测试反馈
- 改进 i18n 翻译

通过 Github issues 报告错误时，请提供尽可能完整的信息，包括工作目录中的日志、图片等文件，log 文件夹中的主日志，系统版本环境，配置文件信息，在线视频链接等。

## 联系
如果您有兴趣为 Score Capture 贡献想法或代码，可以联系 Carrot_shreds@163.com。

## [许可证](LICENSE)
本项目是基于 GPL v3 协议开源的自由软件，禁止闭源的商业售卖与分发。
