---
tags:
  - 类型/MOC
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: baoyu-skills 技能库索引与落地路线（技能卡片 + 工作流）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/**
  - baoyu-skills/**
---

# baoyu-skills（MOC）

`baoyu-skills` 是一组面向“内容获取 → 内容处理 → 视觉生成 → 发布”的 Claude Code Skills。这里以知识库方式沉淀：**每个 skill 一页技能卡片** + **可复用工作流**。

## 快速入口

- 配置约定：[[05-AI技术文档/外部技能库/baoyu-skills/配置/EXTEND与ENV约定]]
- 工作流（优先）：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]

## 技能卡片（按类别）

### Utility（内容处理/转换）

- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-url-to-markdown]]（网页 → Markdown）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-danger-x-to-markdown]]（X/Twitter → Markdown，需同意声明）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]]（Markdown 排版与排错）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-markdown-to-html]]（Markdown → HTML，公众号友好）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-compress-image]]（图片压缩/转 WebP）

### AI Generation（通用图像生成后端）

- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-image-gen]]（OpenAI/Google/DashScope/Replicate）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-danger-gemini-web]]（Gemini Web 逆向 API，需同意声明）

### Content（内容视觉化/发布）

- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-cover-image]]（文章封面图）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-infographic]]（信息图）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-xhs-images]]（小红书图文卡片）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-slide-deck]]（PPT/Slide Deck 图片）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-comic]]（知识漫画）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-article-illustrator]]（文章配图：定位插图点 → 生成）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-wechat]]（发布到公众号）
- [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-x]]（发布到 X）

---

## 源文件入口（需要细节时回看）

> 技能卡片是“可用性摘要”，更完整的流程与参数以源 `SKILL.md` / `references/` 为准。

- 外部库（知识库内副本）：`05-AI技术文档/外部技能库/baoyu-skills/<skill>/SKILL.md`
- 外部库（仓库副本）：`baoyu-skills/skills/<skill>/SKILL.md`

---

**返回** [[05-AI技术文档/外部技能库/_MOC-外部技能库]] | **总览** [[_MOC-知识库总览]]

