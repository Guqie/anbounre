---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 发布到微信公众号（文章/图文），支持 API 或 Chrome CDP 浏览器流程，含环境检查脚本
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-post-to-wechat/SKILL.md
  - baoyu-skills/skills/baoyu-post-to-wechat/SKILL.md
---

# baoyu-post-to-wechat

## 一句话用途

把内容发布到微信公众号：既支持“文章（HTML/Markdown/文本）”，也支持“图文（多图短内容）”；可走 API 或浏览器自动化（Chrome CDP）。

## 何时用（触发信号）

- 你想把一篇 Markdown/HTML 发布到公众号
- 你想发多图短内容（图文）
- 你想把发布流程标准化（主题/作者/评论开关等默认化）

## 输入 / 输出

- 输入：Markdown/HTML 文件路径，或直接文本（会先落成 md 再继续）
- 输出：在公众号草稿箱/发布结果（取决于脚本与参数）

## 用法（脚本入口）

> 该 skill 有多个脚本：图文/文章/API/检查权限。

```bash
# 环境与权限检查（建议首次先跑）
npx -y bun ${SKILL_DIR}/scripts/check-permissions.ts
```

## 依赖与配置

- EXTEND.md：可配置默认主题/配色/发布方式/作者/评论开关/Chrome profile 等（见源 `SKILL.md`）。
- 如果走浏览器发布：需要 Chrome + 可用的粘贴/辅助权限（源 `SKILL.md` 有 pre-flight check）。
- 如果走 API：需要对应的 API 凭证与配置（详见源 `SKILL.md`）。

## 常见坑与排查

- 发布脚本连不上浏览器：先跑 `check-permissions.ts` 看具体缺什么
- 标题/作者/评论开关每次都要手填：在 EXTEND.md 固定默认值

## 最佳搭配

- 上游 Markdown → HTML：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-markdown-to-html]]
- 上游清洗：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-post-to-wechat/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

