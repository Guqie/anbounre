---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 将纯文本/Markdown 清洗成更规范的 Markdown，并进行中英混排排版纠错；默认输出 *-formatted.md
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-format-markdown/SKILL.md
  - baoyu-skills/skills/baoyu-format-markdown/SKILL.md
---

# baoyu-format-markdown

## 一句话用途

把“可读但不规范”的文本/Markdown，整理成更结构化的 Markdown，并执行排版脚本（中英混排空格、强调符号、引号等）。

## 何时用（触发信号）

- 网页/X 抓取出来的 md 很乱、标题/列表/重点不清
- 想补全 frontmatter、标题、摘要等基础结构
- 想修复中英混排空格、中文强调符号、引号样式等排版问题

## 输入 / 输出

- 输入：`.md` 或纯文本文件
- 输出：`{filename}-formatted.md`（默认策略：不破坏原始文件）

## 用法

### CLI（Bun，排版脚本）

> 源技能将“内容结构化（Steps 1-6）”交给 Agent 完成，脚本主要负责排版纠错（Step 7）。

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --quotes
npx -y bun ${SKILL_DIR}/scripts/main.ts article.md --no-spacing
```

## 关键参数（脚本）

- `--quotes`：把 ASCII 引号替换为全角引号（默认关闭）
- `--no-spacing`：不做中英混排空格（默认会做）
- `--no-emphasis`：不修复强调/加粗相关的 CJK 标点问题（默认会做）

## 依赖与配置

- EXTEND.md（可选）：默认排版选项、摘要长度等（见源 `SKILL.md`）

## 常见坑与排查

- **“Typography only” 可能原地修改文件**：在执行前确认你要不要覆盖原稿；更稳妥是先生成 `*-formatted.md` 再处理。
- 格式化过度/不符合个人习惯：优先通过 EXTEND 调整默认策略，或在调用时显式开关 spacing/emphasis/quotes。

## 最佳搭配

- 上游抓取：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-url-to-markdown]]、[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-danger-x-to-markdown]]
- 下游转 HTML：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-markdown-to-html]]
- 工作流：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-format-markdown/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

