---
name: docx2md
description: 将 Word 文档(.docx)转换为 Markdown 格式，支持批量转换、图片提取、表格保留
allowed-tools: Bash, Read, Write, Glob
---

# DOCX → Markdown 转换工具

## 前置依赖

- `pandoc`（已安装：D:\anaconda3\Scripts\pandoc.exe）

## 使用方式

```
/docx2md <文件路径或目录>
```

## 转换流程

### 1. 单文件转换

用户提供 .docx 文件路径时，执行：

```bash
pandoc "<输入文件>.docx" -t gfm --wrap=none --extract-media="<输出目录>/media" -o "<输出文件>.md"
```

参数说明：
- `-t gfm`：输出 GitHub Flavored Markdown（表格友好）
- `--wrap=none`：不自动换行，保持段落完整
- `--extract-media`：提取文档中的图片到 media 子目录

### 2. 批量转换

用户提供目录路径时：
1. 用 Glob 工具搜索 `**/*.docx` 找到所有 docx 文件
2. 逐个执行 pandoc 转换
3. 输出文件放在同目录下，扩展名改为 .md

### 3. 输出位置规则

- 默认：与源文件同目录，同名 .md
- 如用户指定输出路径，使用用户指定的路径
- 图片提取到 `<输出目录>/media/` 下

## 转换后处理

转换完成后自动执行：
1. 读取生成的 .md 文件，检查格式是否正常
2. 如有图片，确认 media 目录中图片已提取
3. 报告转换结果：文件大小、段落数、是否含表格/图片

## 示例

```
/docx2md D:/文档/报告.docx
/docx2md D:/文档/批量目录/
/docx2md D:/文档/报告.docx -o D:/桌面/输出.md
```
