---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 将内容生成 Slide Deck（逐页图片），支持风格预设、只生成大纲/只生成图片、合并为 PPTX/PDF
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-slide-deck/SKILL.md
  - baoyu-skills/skills/baoyu-slide-deck/SKILL.md
---

# baoyu-slide-deck

## 一句话用途

把内容转成可阅读/可分享的“逐页幻灯片图片”，并可合并为 `.pptx` 或 `.pdf`。

## 何时用（触发信号）

- 需要做 PPT，但更偏“可分享的滑动阅读”而非现场演讲
- 想先出大纲/提示词，再决定是否生成图片（partial workflows）
- 想固定风格体系（blueprint/corporate/minimal/notion 等）

## 输入 / 输出

- 输入：Markdown 文件或粘贴内容
- 输出（源文档定义）：`slide-deck/{topic-slug}/`（包含 outline、prompts、png、pptx、pdf）

## 用法（Claude Code）

```bash
/baoyu-slide-deck content.md
/baoyu-slide-deck content.md --style sketch-notes --slides 10
/baoyu-slide-deck content.md --outline-only
```

## 关键参数

- `--style`：风格预设（默认 `blueprint`）
- `--audience`：`beginners/intermediate/experts/executives/general`
- `--slides`：目标页数
- `--outline-only` / `--prompts-only` / `--images-only`
- `--regenerate`：重做指定页

## 依赖与配置

- EXTEND.md（可选）：语言/风格等默认值（见源 `SKILL.md`）

## 常见坑与排查

- 页数不合适：按源 `SKILL.md` 的“内容长度 → 页数”建议先估算，再用 `--slides` 固定
- 想重做个别页：用 `--regenerate`

## 最佳搭配

- 生成后压缩：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-slide-deck/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

