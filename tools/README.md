# tools — IISP 与历史 monorepo 布局

## 主项目：IISP

**IISP**（Industrial Inspection Solutions Platform，工业检测解决方案平台）即本目录下的 **[`DetForge-Studio`](./DetForge-Studio/)** 仓库。

- 产品说明：[`DetForge-Studio/README.md`](./DetForge-Studio/README.md)
- **最终设计定稿**：[`DetForge-Studio/docs/IISP_DESIGN_FINAL.md`](./DetForge-Studio/docs/IISP_DESIGN_FINAL.md)
- **编码规范 / Vibe**：[`DetForge-Studio/docs/CODING_STANDARDS.md`](./DetForge-Studio/docs/CODING_STANDARDS.md) · [`DetForge-Studio/AGENTS.md`](./DetForge-Studio/AGENTS.md)
- 子模块：`DetForge-Studio/packages/`（coco-visualizer、detunify 等，**git submodule 分别管理**）
- 默认端口：**5050**

```bash
cd tools/DetForge-Studio
git submodule update --init --recursive
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
python app.py
```

## 历史布局（迁移中）

外层 `online_data_tool` 曾将 COCOVisualizer、DetUnify-Studio 与 DetForge-Studio 并列放在 `tools/` 下作为 submodule。  
**现行做法**：看图与预测已迁入 **`DetForge-Studio/packages/`**；克隆 IISP 仓库后只需：

```bash
cd tools/DetForge-Studio
git submodule update --init --recursive
```

若仍保留 `tools/COCOVisualizer`、`tools/DetUnify-Studio` 并列目录，IISP 会自动回退解析到 sibling 路径（兼容旧布局）。

## 目录说明

```
tools/
├── README.md                 # 本文件
├── DetForge-Studio/          # IISP 主仓库
│   ├── packages/
│   │   ├── coco-visualizer/  # submodule
│   │   └── detunify/         # submodule
│   ├── studio/               # 主仓能力模块
│   └── frontend/
├── COCOVisualizer/           # （可选）历史外层 submodule，迁移后可移除
└── DetUnify-Studio/          # （可选）历史外层 submodule，迁移后可移除
```

## 添加新的 packages 子模块

在 `DetForge-Studio` 仓库根目录：

```bash
git submodule add git@github.com:<org>/<repo>.git packages/<name>
```

更新 [`DetForge-Studio/packages/README.md`](./DetForge-Studio/packages/README.md) 中的表格。
