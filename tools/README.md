# 外部工具目录

本目录通过 **Git Submodule** 集中管理来自其它 GitHub 仓库的线上数据相关工具。

## 克隆本仓库后初始化子模块

```bash
git submodule update --init --recursive
```

仅更新某一工具：

```bash
git submodule update --remote tools/COCOVisualizer
```

> Submodule 使用 SSH 地址（`git@github.com:...`）。若本机 HTTPS 可用而 SSH 不可用，可在 `.gitmodules` 中改为 `https://github.com/...` 后执行 `git submodule sync`。

## 已收录工具

| 目录 | 用途 | 来源仓库 | 默认端口 |
|------|------|----------|----------|
| [COCOVisualizer](./COCOVisualizer/) | 看图：COCO 浏览、GT/预测对比、标注修正 | [algo-boost/COCOVisualizer](https://github.com/algo-boost/COCOVisualizer) | 6010 |
| [picture-collection](./picture-collection/) | 捞图：数据库查询图片并导出 COCO/CSV | [algo-boost/picture-collection](https://github.com/algo-boost/picture-collection) | 5050 |
| [DetUnify-Studio](./DetUnify-Studio/) | 预测：多模型检测统一预测与结果管理 | [algo-boost/DetUnify-Studio](https://github.com/algo-boost/DetUnify-Studio) | 6006 |

## 快速启动

### COCOVisualizer（看图）

```bash
cd tools/COCOVisualizer
pip install -e .
coco-viz
# 或: python app.py
```

详见 [COCOVisualizer/README.md](./COCOVisualizer/README.md)。

### picture-collection（捞图）

```bash
cd tools/picture-collection
pip install -r requirements.txt
python app.py
# http://localhost:5050
```

启动后在 Web 界面配置数据库与图片路径。详见 [picture-collection/README.md](./picture-collection/README.md)。

### DetUnify-Studio（预测）

```bash
cd tools/DetUnify-Studio/app
pip install flask werkzeug loguru opencv-python numpy
python app.py
# http://localhost:6006
```

命令行预测见 `tools/DetUnify-Studio/src/predict/`。详见 [DetUnify-Studio/README.md](./DetUnify-Studio/README.md)。

## 目录结构

```
tools/
├── README.md
├── COCOVisualizer/       # submodule
├── picture-collection/   # submodule
└── DetUnify-Studio/      # submodule
```

添加新工具：

```bash
git submodule add git@github.com:<org>/<repo>.git tools/<name>
```

然后更新本文档中的表格与快速启动说明。
