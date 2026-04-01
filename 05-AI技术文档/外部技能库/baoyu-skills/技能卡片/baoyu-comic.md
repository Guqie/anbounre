---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 知识漫画生成（art × tone × layout），支持只出分镜/只出 prompts/只出图片与 PDF 合并
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-comic/SKILL.md
  - baoyu-skills/skills/baoyu-comic/SKILL.md
---

# baoyu-comic

## 一句话用途

把知识内容改编成“可读的漫画分镜与逐页图片”，支持多种画风/基调/版式组合，并可合并为 PDF。

## 何时用（触发信号）

- 想把教程/传记/概念讲解做成漫画（更易传播）
- 需要先出分镜确认，再批量生成图片
- 想固定 art/tone/layout 形成统一系列

## 输入 / 输出

- 输入：Markdown 文件或粘贴内容
- 输出（源文档定义）：`comic/{topic-slug}/`（包含 storyboard、characters、prompts、png、pdf）

## 用法（Claude Code）

```bash
/baoyu-comic article.md
/baoyu-comic article.md --art manga --tone warm
```

## 关键参数

- `--art`：`ligne-claire`（默认）、`manga/realistic/ink-brush/chalk`
- `--tone`：`neutral`（默认）、`warm/dramatic/romantic/energetic/vintage/action`
- `--layout`：`standard/cinematic/dense/splash/mixed/webtoon`
- `--storyboard-only` / `--prompts-only` / `--images-only`
- `--regenerate`：重做指定页

## 依赖与配置

- EXTEND.md（BLOCKING）：首次需要完成偏好设置（见源 `SKILL.md` 的 1.1 Preferences）。
- 角色参考图：源工作流要求先生成 `characters/characters.png`，再用它作为后续页的 `--ref`（确保风格一致）。

## 常见坑与排查

- 人物长相不一致：确保按源流程先生成并复用角色参考图
- 想节省成本：先 `--storyboard-only` 确认再生成图片

## 最佳搭配

- 生成后压缩：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-comic/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

