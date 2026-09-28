# DIKWP NeuroWeave Lab 中文入口

[在线项目页](https://yucongduan.github.io/DIKWP-NeuroWeave-Lab/) · [完整版本下载](https://github.com/YucongDuan/DIKWP-NeuroWeave-Lab/releases/tag/v1.0.0) · [English](README.md)

让章节成为可复现的实验。本系统提供 18 章实验、可重构记忆、证据评估、意图关联计划和本地同意流程。

在线页面可直接阅读随附的合成实验报告。需要修改参数、重新计算或操作完整界面时，请下载并解压 ZIP，在项目目录中使用 Python 3.11 及以上版本运行：

```bash
python -m neuroweave list
python -m neuroweave run chapter-10 --out outputs/my-lab
python -m neuroweave serve --port 8765
```

启动服务器后打开 `http://127.0.0.1:8765`；关闭时按 Ctrl+C。源码运行不需要安装第三方运行时依赖、API 密钥或下载模型。

本次发布运行了 155 项本地测试并全部通过。19 份参考 JSON 已完整复现，包括 20 个种子的合成基准。 持续集成的实际平台和提交结果请查看 [GitHub Actions](https://github.com/YucongDuan/DIKWP-NeuroWeave-Lab/actions)。

[英文手册](NeuroWeave_English_Handbook.pdf) · [运行指南](GETTING_STARTED.md) · [发布记录](PUBLICATION_2026-09-28.md) · [全部项目](https://github.com/YucongDuan/YucongDuan/blob/main/REPOSITORY_DIRECTORY.zh-CN.md)

原始代码和文档许可为 MIT，保留原作者及贡献者署名。模型用于研究与教学，合成实验结果不构成临床效果、完整大脑模拟或主观体验的证明。
