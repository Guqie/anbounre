---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 通过真实 Chrome（CDP）发布到 X：普通推文/图文/视频/引用推文/X Articles（长文）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-post-to-x/SKILL.md
  - baoyu-skills/skills/baoyu-post-to-x/SKILL.md
---

# baoyu-post-to-x

## 一句话用途

用真实 Chrome 浏览器（CDP）发布到 X：支持普通推文（含图）、视频推文、引用推文，以及 X Articles（长文）。

## 何时用（触发信号）

- 想把内容一键填入 X 发布界面（但仍由你最终确认发布）
- 想发带图/带视频的推文
- 你有 X Premium，需要发布长文（X Articles）

## 输入 / 输出

- 输入：文本、图片/视频路径，或文章 Markdown
- 输出：浏览器打开并填充内容（通常由用户手动点击发布）

## 用法（脚本入口）

```bash
# 普通推文（文字 + 图片）
npx -y bun ${SKILL_DIR}/scripts/x-browser.ts "Hello!" --image ./photo.png

# 视频推文
npx -y bun ${SKILL_DIR}/scripts/x-video.ts "Check this out!" --video ./clip.mp4

# 引用推文
npx -y bun ${SKILL_DIR}/scripts/x-quote.ts https://x.com/user/status/123 "Great insight!"

# X Articles（长文）
npx -y bun ${SKILL_DIR}/scripts/x-article.ts article.md
```

## 依赖与配置

- 依赖：Chrome + `bun`；首次需要手动登录一次（会话缓存）。
- EXTEND.md（可选）：默认 Chrome profile 等。
- 可选检查：`npx -y bun ${SKILL_DIR}/scripts/check-paste-permissions.ts`

## 常见坑与排查

- `Chrome debug port not ready`：通常是残留 CDP 实例冲突；先关闭相关 Chrome 再重试（源 `SKILL.md` 有处理建议）。

## 最佳搭配

- 上游内容处理：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]
- 长文发布前转 HTML：可参考该 skill 内置的 `md-to-html.ts` 或用 [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-markdown-to-html]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-post-to-x/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

