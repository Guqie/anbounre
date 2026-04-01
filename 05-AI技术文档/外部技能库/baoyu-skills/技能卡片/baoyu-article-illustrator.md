---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 为文章“定位需要配图的位置”并按 type × style 生成配图，输出 outline + prompts + 图片
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-article-illustrator/SKILL.md
  - baoyu-skills/skills/baoyu-article-illustrator/SKILL.md
---

# baoyu-article-illustrator

## 一句话用途

读懂文章结构，找出“哪里该配图、配什么图”，再按 **Type（信息结构）× Style（视觉风格）** 生成成套插图，并给出可追溯的 outline/prompts。

## 何时用（触发信号）

- 文章需要配图提升理解（流程图、框架图、对比图、时间线等）
- 想保证整篇文章插图风格一致（固定 style）
- 你希望“先确认插图策略”，再生成图片（可控、可复用）

## 输入 / 输出

- 输入：文章 Markdown 文件或粘贴内容
- 输出（源文档定义）：`illustrations/{topic-slug}/`（含 `outline.md`、`prompts/`、`NN-*.png`）

## 用法（Claude Code）

```bash
/baoyu-article-illustrator article.md
/baoyu-article-illustrator article.md --type infographic --style blueprint
/baoyu-article-illustrator article.md --density rich
```

## 关键参数

- `--type`：`infographic/scene/flowchart/comparison/framework/timeline/mixed`
- `--style`：见源 `references/styles.md`
- `--density`：`minimal/balanced/rich`

## 依赖与配置

- EXTEND.md（BLOCKING）：首次需要配置默认输出目录/水印/偏好 type/style 等（见源 `SKILL.md`）。
- 图像后端：通常会调用 `baoyu-image-gen`（建议先把其 provider/model 配好）。

## 常见坑与排查

- 插图“字面化”：源文档强调 **metaphor 要可视化底层概念，而不是画字面物体**；不对就回看 `references/workflow.md`。
- 风格漂移：固定 `--style`，并尽量复用同一套 core style 规则。

## 最佳搭配

- 图像后端：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-image-gen]]
- 封面：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-cover-image]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-article-illustrator/SKILL]]
- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-article-illustrator/references/usage]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

