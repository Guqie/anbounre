---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 将 Markdown 转成带内联 CSS 的 HTML（公众号友好主题，支持代码高亮/脚注/告警块等）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-markdown-to-html/SKILL.md
  - baoyu-skills/skills/baoyu-markdown-to-html/SKILL.md
---

# baoyu-markdown-to-html

## 一句话用途

把 Markdown 转成“可直接发布/粘贴”的 HTML（内联 CSS），并支持常见增强语法（代码高亮、脚注、告警块、Mermaid/PlantUML 等）。

## 何时用（触发信号）

- 需要把 md 变成公众号/平台更友好的 HTML
- 想统一套用主题（theme）与主色（color）
- 下游要交给 `post-to-wechat` / `post-to-x` 的文章发布脚本

## 输入 / 输出

- 输入：Markdown 文件
- 输出：同目录同名 `.html`
  - 若目标 html 已存在：先备份为 `.bak-YYYYMMDDHHMMSS`

## 用法

### CLI（Bun）

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --theme grace
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --theme modern --color red
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --keep-title
```

## 关键参数

- `--theme <name>`：`default/grace/simple/modern`
- `--color <preset|hex>`：主色（预设或 hex）
- `--keep-title`：保留正文第一条标题（默认会移除，避免与 frontmatter title 重复）
- `--title <text>`：覆盖 title

## 依赖与配置

- EXTEND.md（可选）：可配置默认主题/颜色等；避免每次手选（细节见源 `SKILL.md`）

## 常见坑与排查

- 标题重复：检查 frontmatter 是否有 `title`，以及是否需要 `--keep-title`
- 主题每次都要选：在 EXTEND.md 配 `default_theme`

## 最佳搭配

- 上游清洗：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]]
- 下游发布：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-wechat]]、[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-post-to-x]]
- 工作流：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-markdown-to-html/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

