---
name: fix-frontmatter
description: 批量为缺失 frontmatter 的 Markdown 文件注入标准化 YAML 头（标签、日期、状态）
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 批量修复 Frontmatter

## 目标

扫描知识库中所有 `.md` 文件，为缺失 frontmatter 的文件注入标准化 YAML 头。

## 排除目录

以下目录不处理：
- `.git/`、`.obsidian/`、`.spec-workflow/`、`.trae/`、`.claude/`
- `node_modules/`、`templates/`、`tools/`

以下文件不处理：
- `README.md`、`CLAUDE.md`、`PROJECT_KNOWLEDGE.md`

## 执行流程

### Step 1: 扫描

用 Glob 搜索 `**/*.md`，逐个读取文件开头，判断是否已有 frontmatter（以 `---` 开头）。
收集所有缺失 frontmatter 的文件路径列表。

### Step 2: 分类打标

根据文件路径，按以下映射规则确定 `类型/` 标签：

```
08-大脑核心/**                → 类型/记忆
09-灵魂系统/**                → 类型/灵魂系统
05-AI技术文档/提示词工程/**    → 类型/提示词
05-AI技术文档/提示词收集库/**  → 类型/提示词
05-AI技术文档/技术文档/**      → 类型/工具技巧
01-研究方法论/**               → 类型/方法论
00-每日工作区/00-今日任务/**   → 类型/日志
00-每日工作区/02-信顾业务/**   → 类型/项目
06-个人成长/职业规划/**        → 类型/方法论
10-个人日记/**                 → 类型/日志
_MOC-*                         → 类型/MOC
```

未匹配到的文件，根据所在顶级目录推断：
- `02-政策于宏观库/` → 类型/方法论 + 领域/政策
- `03-行业研究库/` → 类型/方法论 + 领域/行业
- `04-专题研究库/` → 类型/方法论
- `06-个人成长/` → 类型/方法论
- `07-完成归档/` → 类型/方法论 + 状态/归档
- 其他 → 类型/方法论（默认）

### Step 3: 状态推断

读取文件内容判断状态：
- 文件内容少于 50 字符（去除标题和空行后）→ `状态/草稿`
- 包含 `{{` 模板占位符 → `状态/草稿`
- `07-完成归档/` 下的文件 → `状态/归档`
- 其他 → `状态/活跃`

### Step 4: 日期获取

优先使用 git log 获取文件首次提交时间：
```bash
git log --diff-filter=A --follow --format=%aI -1 -- "<文件路径>"
```

如果 git 无记录（未跟踪文件），使用当前日期。

### Step 5: 注入 Frontmatter

在文件开头插入以下格式的 YAML 头：

```yaml
---
tags:
  - 类型/xxx
  - 状态/xxx
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

注意事项：
- 如果文件第一行是 `# 标题`，frontmatter 插入在标题之前
- 保留文件原有内容不变
- 如果文件已有 frontmatter 但缺少 tags 字段，补充 tags 而非覆盖整个 frontmatter

### Step 6: 报告

处理完成后输出汇总：
- 总扫描文件数
- 已有 frontmatter 的文件数（跳过）
- 新注入 frontmatter 的文件数
- 按类型标签分组统计

## 安全机制

- 每处理 5 个文件后暂停，报告进度
- 如果检测到文件内容异常（二进制、超大文件 >100KB），跳过并报告
- 不修改 `templates/` 目录下的模板文件
