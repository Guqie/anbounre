---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: baoyu-skills 的偏好配置（EXTEND.md）与密钥（.env）加载约定汇总
---

# EXTEND 与 ENV 约定（baoyu-skills）

> 目的：减少每个技能卡片重复描述；所有“路径/优先级/通用注意事项”在这里统一。

## EXTEND.md（偏好设置）

多数 skills 支持 `EXTEND.md`（可选或阻塞式必填）。常见查找顺序：

1. 项目级：`.baoyu-skills/<skill>/EXTEND.md`
2. 用户级：`$HOME/.baoyu-skills/<skill>/EXTEND.md`

> 个别技能（例如 `baoyu-danger-x-to-markdown`）在 EXTEND 不存在时是 **BLOCKING**：必须先做首次设置，不能直接用默认值继续跑。

## .env（密钥/环境变量）

部分 skills 依赖 API Key（例如 `baoyu-image-gen`）。常见加载路径（以源文档为准）：

- `<cwd>/.baoyu-skills/.env`
- `~/.baoyu-skills/.env`

并叠加各 Provider 的环境变量（例如 `OPENAI_API_KEY`、`GOOGLE_API_KEY` 等）。

## 逆向/非官方 API 的同意文件（Consent）

以下技能在首次使用前需要用户明确同意声明（Consent），并在本机写入同意文件：

- `baoyu-danger-x-to-markdown`：X/Twitter 逆向 API（同意后才允许转换）
- `baoyu-danger-gemini-web`：Gemini Web 逆向 API（同意后才允许调用）

> 这类技能的“可用性”受平台策略影响更大：随时可能失效；出问题优先回看对应源 `SKILL.md` 的 Consent 章节。

## 常用排错清单（通用）

- Chrome/CDP 类技能报找不到浏览器：先检查是否安装 Chrome，再看是否支持设置 `<SKILL>_CHROME_PATH`（各技能名不同）。
- “Chrome debug port not ready / Unable to connect”：通常是残留的 CDP 实例；先关闭相关 Chrome，再重试。
- 输出目录冲突：多数技能会自动在 slug 后追加时间戳（`-YYYYMMDD-HHMMSS`）。

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

