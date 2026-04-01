---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 用 Chrome CDP 抓取任意网页并转成干净 Markdown（支持登录页等待模式）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-url-to-markdown/SKILL.md
  - baoyu-skills/skills/baoyu-url-to-markdown/SKILL.md
---

# baoyu-url-to-markdown

## 一句话用途

把网页（含 JS 渲染）抓取为可归档的 Markdown；遇到需要登录/懒加载可用等待模式再截取。

## 何时用（触发信号）

- 需要把某个 URL 保存为本地 Markdown
- 网页必须等 JS 渲染完成才能看到正文
- 网页需要登录后才能看到内容（用 `--wait`）

## 输入 / 输出

- 输入：`<url>`
- 输出：
  - 默认：`url-to-markdown/<domain>/<slug>.md`
  - 或用 `-o` 指定输出文件路径

## 用法

### CLI（Bun）

```bash
# 自动模式：页面加载完成后抓取（默认）
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>

# 等待模式：适合登录页/懒加载
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --wait

# 指定输出文件
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md
```

## 关键参数

- `--wait`：等待用户确认页面已准备好再抓取
- `-o <path>`：指定输出路径
- `--timeout <ms>`：加载超时（默认 30000）

## 依赖与配置

- 依赖：Chrome（或可配置自定义路径，见源 `SKILL.md` 的 env 变量）
- EXTEND.md（可选）：默认输出目录、默认 capture mode、timeout（见源 `SKILL.md`）

## 常见坑与排查

- 抓到的内容不完整：改用 `--wait`，等滚动/加载完再抓
- 超时：增大 `--timeout`，或用等待模式

## 最佳搭配

- 抓取后清洗排版：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-format-markdown]]
- 需要发布 HTML：[[05-AI技术文档/外部技能库/baoyu-skills/技能卡片/baoyu-markdown-to-html]]
- 工作流：[[05-AI技术文档/外部技能库/baoyu-skills/工作流/内容处理链路]]

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-url-to-markdown/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

