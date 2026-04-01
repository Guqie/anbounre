---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 将 X/Twitter 推文/线程/长文转换为带 YAML frontmatter 的 Markdown（含媒体下载选项，需同意声明）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-danger-x-to-markdown/SKILL.md
  - baoyu-skills/skills/baoyu-danger-x-to-markdown/SKILL.md
---

# baoyu-danger-x-to-markdown

## 一句话用途

把 `x.com/twitter.com` 的推文/线程/文章提取为 Markdown，并可选择把媒体资源下载到本地重写链接，便于长期归档。

## 何时用（触发信号）

- 给出 `https://x.com/.../status/...` 或 `twitter.com/.../status/...` 想转成 Markdown
- 想把推文当作“信源”落到知识库
- 需要把图片/视频也本地化保存

## 输入 / 输出

- 输入：推文/文章 URL
- 输出（源文档定义）：`x-to-markdown/{username}/{tweet-id}/{content-slug}.md`
  - 可选：`imgs/`、`videos/`（开启下载媒体时）

## 用法

### CLI（Bun）

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --download-media
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --json
```

## 关键参数

- `-o <path>`：指定输出路径
- `--download-media`：把媒体下载到本地并重写 Markdown 链接
- `--login`：仅刷新 cookies（不做转换）
- `--json`：JSON 输出

## 依赖与配置

- **Consent（必须）**：首次使用前需要同意声明（逆向 API 风险），否则不应继续转换（见源 `SKILL.md` 的 Consent Requirement）。
- EXTEND.md（可能是 BLOCKING）：首次没有 EXTEND 时需要选择媒体处理策略、默认输出目录、保存位置。
- 认证：优先用环境变量（`X_AUTH_TOKEN`、`X_CT0`），或用 Chrome 登录缓存 cookies（见源 `SKILL.md`）。

## 常见坑与排查

- 失效/抓不到：逆向 API 可能被平台调整影响；先回看源 `SKILL.md` 的提示与版本声明
- 媒体没下载：确认是否开启 `--download-media` 或 EXTEND 的 `download_media` 策略

## 最佳搭配

- 转完后清洗排版：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]]
- 工作流：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-danger-x-to-markdown/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

