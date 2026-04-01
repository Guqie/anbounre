---
tags:
  - 类型/工具技巧
  - 状态/活跃
  - 领域/技术
  - 模型/Claude
created: 2026-03-01
updated: 2026-03-01
description: 压缩图片并转换为 WebP/PNG/JPEG（自动选择最佳工具链）
source:
  - 05-AI技术文档/外部技能库/baoyu-skills/baoyu-compress-image/SKILL.md
  - baoyu-skills/skills/baoyu-compress-image/SKILL.md
---

# baoyu-compress-image

## 一句话用途

批量或单张压缩图片，默认转 WebP，减少体积以适配发布（小红书/公众号/网页）。

## 何时用（触发信号）

- 图片太大、加载慢，需要优化体积
- 想统一把 PNG/JPG 转成 WebP
- 需要递归压缩某个目录下的素材

## 输入 / 输出

- 输入：文件或目录
- 输出：默认同路径新扩展名（例如 `image.png → image.webp`），也可用 `--output` 指定

## 用法

### CLI（Bun）

```bash
npx -y bun ${SKILL_DIR}/scripts/main.ts image.png
npx -y bun ${SKILL_DIR}/scripts/main.ts image.png -f png --keep
npx -y bun ${SKILL_DIR}/scripts/main.ts ./images/ -r -q 75
```

## 关键参数

- `--format/-f`：`webp/png/jpeg`（默认 webp）
- `--quality/-q`：0-100（默认 80）
- `--keep/-k`：保留原文件（默认不保留）
- `--recursive/-r`：目录递归

## 依赖与配置

- EXTEND.md（可选）：默认格式/质量/是否保留原图（见源 `SKILL.md`）

## 常见坑与排查

- 质量/清晰度不满意：调高 `--quality` 或改用 `png/jpeg`
- 目录没递归：加 `-r`

## 最佳搭配

- `xhs-images/infographic/slide-deck` 等图像产出后统一压缩

## 参考

- [[05-AI技术文档/外部技能库/baoyu-skills/baoyu-compress-image/SKILL]]

---

**返回** [[05-AI技术文档/外部技能库/baoyu-skills/_MOC-baoyu-skills]]

