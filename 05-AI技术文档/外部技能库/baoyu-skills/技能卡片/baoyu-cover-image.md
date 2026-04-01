---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 文章封面图生成（type/palette/rendering/text/mood/font + aspect），支持快速模式与参考图
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-cover-image/SKILL.md
  - baoyu-skills/skills/baoyu-cover-image/SKILL.md
---

# baoyu-cover-image

## 一句话用途

为文章生成封面图（五维度可控：type/palette/rendering/text/mood + font），支持指定比例与参考图。

## 何时用（触发信号）

- 需要文章封面图（公众号/X/小红书/博客）
- 想统一“封面风格系统”，而不是每次临时想 prompt
- 希望一键快速生成（`--quick`）

## 输入 / 输出

- 输入：文章 Markdown 文件路径或直接粘贴内容
- 输出：按偏好设置选择输出目录（常见是 `cover-image/{topic-slug}/cover.png`，详见源 `SKILL.md`）

## 用法（Claude Code）

```bash
/baoyu-cover-image article.md
/baoyu-cover-image article.md --quick
/baoyu-cover-image article.md --type conceptual --palette warm --rendering flat-vector
/baoyu-cover-image article.md --style blueprint
/baoyu-cover-image article.md --ref style-ref.png
```

## 关键参数

- `--type`：`hero/conceptual/typography/metaphor/scene/minimal`
- `--palette`：`warm/elegant/cool/dark/earth/vivid/pastel/mono/retro`
- `--rendering`：`flat-vector/hand-drawn/painterly/digital/pixel/chalk`
- `--aspect`：`16:9`（默认）、`2.35:1`、`1:1` 等
- `--quick`：跳过确认，直接按自动推荐生成

## 依赖与配置

- EXTEND.md（BLOCKING）：首次需要设置偏好（输出目录/水印/默认维度等），否则不应继续生成（见源 `SKILL.md`）。

## 常见坑与排查

- 风格不稳定：优先用 `--style` 或在 EXTEND 固定默认组合
- 输出目录不符合习惯：在 EXTEND 调整 `default_output_dir`

## 最佳搭配

- 生成后压缩：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]
- 下游发布：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-wechat]]、[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-x]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-cover-image/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

