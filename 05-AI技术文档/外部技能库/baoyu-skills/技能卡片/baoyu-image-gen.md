---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 官方 API 图像生成后端（OpenAI/Google/DashScope/Replicate），支持参考图与比例
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-image-gen/SKILL.md
  - baoyu-skills/skills/baoyu-image-gen/SKILL.md
---

# baoyu-image-gen

## 一句话用途

统一的“图像生成 SDK”：用 API（OpenAI/Google/DashScope/Replicate）生成图片，支持参考图、比例、质量预设；多数视觉类技能会依赖它。

## 何时用（触发信号）

- 你需要直接生成/改图（text-to-image、带参考图）
- 其他技能提示需要图像后端或需要设置默认模型/provider
- 你希望固定默认 provider/model，减少每次选择

## 输入 / 输出

- 输入：prompt（文本/文件）+ 输出图片路径（必填 `--image`）
- 输出：指定的图片文件；可用 `--n` 生成多张

## 用法

### CLI（Bun）

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A landscape" --image out.png --ar 16:9
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Make blue" --image out.png --ref source.png
```

## 关键参数

- `--provider`：`google|openai|dashscope|replicate`
- `--model/-m`：指定模型（或走 EXTEND 默认）
- `--ar`：比例（`16:9`、`1:1`、`9:16` 等）
- `--quality` / `--imageSize`：质量/尺寸预设
- `--ref`：参考图（对 provider/model 有要求，见源 `SKILL.md`）

## 依赖与配置

- **Step 0: Preferences（BLOCKING）**：首次必须完成 EXTEND.md（默认 provider/model/质量等），否则不应开始生成。
- API Key：按 provider 配置 `OPENAI_API_KEY` / `GOOGLE_API_KEY` / `DASHSCOPE_API_KEY` / `REPLICATE_API_TOKEN`。
- `.env` 与 EXTEND 的优先级：见 [[05-AI技术文档/外部技能库/baoyu-skills/配置/EXTEND与ENV约定]]

## 常见坑与排查

- 缺少 API Key：先补齐 `.baoyu-skills/.env` 或 `~/.baoyu-skills/.env`
- 参考图不生效：检查 provider/model 是否支持（源 `SKILL.md` 有明确支持矩阵）

## 最佳搭配

- 作为 `cover-image / infographic / xhs-images / slide-deck / comic / article-illustrator` 的通用后端

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-image-gen/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

