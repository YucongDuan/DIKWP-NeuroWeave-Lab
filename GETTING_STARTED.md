# Run DIKWP NeuroWeave Lab

[Online project home](https://yucongduan.github.io/DIKWP-NeuroWeave-Lab/) · [Versioned downloads](https://github.com/YucongDuan/DIKWP-NeuroWeave-Lab/releases/tag/v1.0.0) · [中文](README.zh-CN.md)

1. Download the versioned ZIP or clone this repository and open its project directory.
2. Use Python 3.11 or later. The source application has no third-party runtime dependencies.
3. Run the following commands in that directory:

```bash
python -m neuroweave list
python -m neuroweave run chapter-10 --out outputs/my-lab
python -m neuroweave serve --port 8765
```

Open `http://127.0.0.1:8765` to use the local workbench. Stop it with Ctrl+C. The online GitHub Pages site serves the supplied result reports; it does not run the Python server or accept research data.

To use the packaged distribution, create an isolated Python environment and install the wheel from the release with `python -m pip install --no-deps <downloaded-wheel.whl>`. The `neuroweave` command is then available.

```bash
python -m unittest discover -s tests -v
python scripts/verify_release.py
```

Read [the original guide](docs/HANDBOOK.md) and [the English handbook](NeuroWeave_English_Handbook.pdf) for input formats, examples and model limitations. Do not overwrite supplied reference results when creating your own runs.
