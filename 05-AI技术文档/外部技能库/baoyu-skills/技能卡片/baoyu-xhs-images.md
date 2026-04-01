---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 小红书图文卡片生成（1-10 张），style × layout 两维组合，适合内容拆解传播
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-xhs-images/SKILL.md
  - baoyu-skills/skills/baoyu-xhs-images/SKILL.md
---

# baoyu-xhs-images

## 一句话用途

把内容拆成 1-10 张“小红书风格”图文卡片，按 **style（审美）× layout（信息结构）** 组合生成系列图片。

## 何时用（触发信号）

- 想把文章/清单/方法论做成“小红书可发”的系列卡片
- 想要多套风格与布局候选再选定
- 需要“信息密度可控”的视觉化输出

## 输入 / 输出

- 输入：Markdown 文件或直接粘贴内容
- 输出（源文档定义）：`xhs-images/{topic-slug}/`（包含分析、3 套大纲策略、prompts 与 PNG）

## 用法（Claude Code）

```bash
/baoyu-xhs-images article.md
/baoyu-xhs-images article.md --style notion
/baoyu-xhs-images article.md --layout dense
/baoyu-xhs-images article.md --style bold --layout comparison
```

## 关键参数

- `--style`：`cute/fresh/warm/bold/minimal/retro/pop/notion/chalkboard/study-notes`
- `--layout`：`sparse/balanced/dense/list/comparison/flow/mindmap/quadrant`

## 依赖与配置

- EXTEND.md（BLOCKING）：首次必须完成偏好设置后再进入分析与风格选择（见源 `SKILL.md` 的 Step 0）。

## 常见坑与排查

- 密度不对：优先调 `--layout`（dense/list 更适合干货）
- 风格不统一：固定 `--style`，并尽量复用同一套元素策略

## 最佳搭配

- 上游清洗：先用 [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]] 把文本结构化
- 生成后压缩：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-xhs-images/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

