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
    <image src="/docs/screenshot/preview.png"/, alt="Tab Preview">
    <image src="/docs/screenshot/stitch.png"/, alt="Tab Stitch">
    <image src="/docs/screenshot/reclip.png"/, alt="Tab Reclip">
    <image src="/docs/screenshot/settings.png"/, alt="Tab Settings">
</details>

## 特性
- [x] 基于窗口的动态预览定位
- [x] 基于MVVM数据绑定的响应式ui 
- [x] 基于QtAds的docking布局
- [x] 调用MSS库或命令行工具实现跨平台截图
- [x] 识别谱线并自动化拼接
- [x] 易用的手动拼接调整工具
- [x] 基础输出样式编辑
- [ ] 多线程计算，异步文件加载
- [ ] 直接从视频文件中提取图片
- [ ] 基于鼠标框选的定位系统
- [ ] 更加完善的跨平台支持
- [ ] i18n支持
- [ ] 五线谱优化
- [ ] 多音轨支持
- [ ] 单文件编译构建

## 从源码运行/开发

获取源码并进去项目根目录

    git clone https://github.com/Carrot-shreds/score_capture.git
    cd score_capture

安装uv环境

    pip install uv 
    或
    curl -LsSf https://astral.sh/uv/install.sh | sh

同步构建环境（默认不包含开发依赖）

    uv sync
    或
    uv sync --dev

运行程序入口

    uv run main.py
    (Linux) bash main.sh

获取仓库更新

    git pull

从源码编译构建exe

    uv run ./build.py

## 工作流程
0. 使用output_dir//score_title作为工作目录。
1. 通过定位窗口获取曲谱位置。
2. 通过预览窗口预览范围和线段识别参数（可选）
3. 打开截图，播放视频，关闭截图．在此过程中，每隔指定时间截图生成一张capture\*.\*图像。之后将两张以上"相同"(比较相似度)capture生成一张image\*.\*。
4. 使用设置的参数对每张image进行线段识别，生成image-detected以及ScoreDetections.json，主要需要用到小节线(即竖直线)的位置做参考。
5. 以各小节线前后的范围为参考，拼接相邻的image，比较获得两张图像重叠最"完美"的位置，保存到ScoreStitchData.json，并拼接生成title-stitched。
6. 对title-stitched进行线段检测，生成title-stitched-detected，与title-stitched-barlines，主要也是获得拼接图中的小节线，用来将横向的长图从小节线前后切开，重新排版到竖向，生成title-reclip
7. 对title-reclip按打印比例切分，添加边距/标题/页码等样式，最终生成title*.*

## FAQ
### Score capture是跨平台的吗？
是的，本项目基于python与PySide(Qt的python绑定)，设计上能够支持Windows/MacOS/Linux系统桌面端跨平台。但是目前除windows外的测试仍然比较欠缺，可能会一定的兼容性问题。
### 为什么Win7系统无法运行？
Python官方在3.9版本之后放弃了对于win7的支持，如果需要移植适配，需要降级到python=3.8版本，暂时并没有这个计划。
### 为什么我的fcitx输入法打不出字？
在linux上运行时请使用`bash main.sh`启动主程序，以确保加载libfcitx5插件。如果预编译插件加载失败，尝试使用`bash fcitx5-qt.sh`重新编译。
### 它支持xxx类型的曲谱吗?
考虑到曲谱类型的多样，以及视频质量的不同，开发测试通常无法覆盖全部情况。开发将会优先考虑**横向滚动的TAB曲谱**，而关于纵向滚动，五线谱等其他类型的支持，则需要通过更多的用户测试与反馈进行改善。如果遇到了问题，请尝试使用手动拼接工具，或是将其作为一个issue进行反馈。

## 贡献
本项目仍在持续开发当中，欢迎各种形式的贡献，包括但不限于：
- 报告漏洞
- 新功能建议
- 跨平台测试反馈
- 提供i18n翻译

报告错误时，请提供尽可能完整的信息，包括工作目录下的日志、log文件夹中的主日志、配置文件信息、视频链接或图片等。

## [许可证](LICENSE)
本项目是基于GPL v3协议开源的自由软件，禁止闭源的商业售卖与二次分发.
