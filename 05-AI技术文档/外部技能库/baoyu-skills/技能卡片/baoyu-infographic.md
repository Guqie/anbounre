---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 信息图生成（layout × style），适合把内容做成可发布的单张图总结
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-infographic/SKILL.md
  - baoyu-skills/skills/baoyu-infographic/SKILL.md
---

# baoyu-infographic

## 一句话用途

把内容转成“可发布的信息图”：通过 **layout（结构）× style（视觉）** 两维组合生成单张信息图。

## 何时用（触发信号）

- 想把文章/报告做成一张信息图（便于传播）
- 需要“结构化视觉表达”（时间线、对比、金字塔、仪表盘等）
- 想按内容自动推荐 layout/style，然后再人工确认

## 输入 / 输出

- 输入：Markdown 文件或粘贴内容
- 输出（源文档定义）：`infographic/{topic-slug}/infographic.png`（并包含 analysis/structured-content/prompt 等过程文件）

## 用法（Claude Code）

```bash
/baoyu-infographic path/to/content.md
/baoyu-infographic path/to/content.md --layout hierarchical-layers --style technical-schematic
/baoyu-infographic path/to/content.md --aspect portrait --lang zh
```

## 关键参数

- `--layout`：21 种（默认 `bento-grid`）
- `--style`：20 种（默认 `craft-handmade`）
- `--aspect`：`landscape(16:9)` / `portrait(9:16)` / `square(1:1)`
- `--lang`：`zh/en/ja/...`

## 依赖与配置

- EXTEND.md（可选）：默认风格/语言等（见源 `SKILL.md`）

## 常见坑与排查

- 信息太密/太散：优先换 `layout`（而不是只换 `style`）
- 想做“高密度指南图”：用 layout `dense-modules` + 选推荐 style（源 `SKILL.md` 有关键词快捷方式）

## 最佳搭配

- 生成后压缩：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]
- 多图/系列传播：也可用 `xhs-images` 做成 1-10 张系列卡片

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-infographic/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

