---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 通过 Gemini Web 逆向 API 生成文本/图片（支持参考图与多轮会话，需同意声明）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-danger-gemini-web/SKILL.md
  - baoyu-skills/skills/baoyu-danger-gemini-web/SKILL.md
---

# baoyu-danger-gemini-web

## 一句话用途

用 Gemini Web 逆向 API 做文本/图片生成，支持参考图（vision）与多轮会话；适合作为“无官方 key 的临时后端”，但稳定性与风险更高。

## 何时用（触发信号）

- 需要用 Gemini Web 来生成文本或图片
- 其他技能提示需要 Gemini Web 后端（或你想用它替代某些 provider）
- 你没有/不想用官方 API Key 的方案

## 输入 / 输出

- 输入：`--prompt`（或直接 positional prompt）
- 输出：文本（stdout）或图片（`--image` 指定路径）

## 用法

### CLI（Bun）

```bash
# 文本
npx -y bun ${SKILL_DIR}/scripts/main.ts "Your prompt"

# 生成图片
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cute cat" --image cat.png

# 参考图（vision）
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Describe this" --reference image.png
```

## 关键参数

- `--model/-m`：`gemini-3-pro`（默认）、`gemini-3-flash` 等
- `--image [path]`：生成图片
- `--reference/--ref`：参考图输入
- `--sessionId`：多轮会话
- `--json`：JSON 输出

## 依赖与配置

- **Consent（必须）**：首次使用前要同意声明并写入 consent 文件（Windows/macOS/Linux 路径见源 `SKILL.md`）。
- 认证：首次会打开浏览器登录 Google，cookies 会缓存。
- EXTEND.md（可选）：默认 model、代理、数据目录等。

## 常见坑与排查

- 无法访问 Google：配置 `HTTP_PROXY/HTTPS_PROXY`
- 同意文件缺失/版本不匹配：重新走 consent 流程

## 最佳搭配

- 需要 vision + 多轮时的“替补后端”；如追求稳定优先用 [[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-image-gen]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-danger-gemini-web/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

