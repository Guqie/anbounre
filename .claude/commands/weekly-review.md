---
name: weekly-review
description: 每周自动生成知识库复盘报告，统计本周新增/修改/孤立文档，给出改进建议
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 知识库周复盘

## 目标

自动生成本周知识库变更复盘报告，帮助用户了解知识库健康趋势。

## 执行流程

### Step 1: 收集本周变更

通过 git log 获取最近 7 天的文件变更：

```bash
git log --since="7 days ago" --name-status --pretty=format:"%h|%ai|%s" -- "*.md"
```

分类统计：
- **新增文件 (A)**：本周新建的文档
- **修改文件 (M)**：本周编辑过的文档
- **删除文件 (D)**：本周删除的文档

### Step 2: 运行审计快照

调用 `tools/kb_audit.ps1` 获取当前指标，并与 CSV 历史对比：

```bash
powershell -ExecutionPolicy Bypass -File ./tools/kb_audit.ps1
```

从 `tools/kb-audit-history.csv` 读取最近两条记录，计算趋势。

### Step 3: 生成复盘报告

输出到 `00-每日工作区/00-今日任务/` 目录，文件名格式：`周复盘_YYYY-MM-DD.md`

报告结构：

```markdown
---
tags:
  - 类型/日志
  - 状态/活跃
created: YYYY-MM-DD
---

# 📊 知识库周复盘 (YYYY-MM-DD)

## 本周变更概览
| 指标 | 数值 |
|------|------|
| 新增文档 | X |
| 修改文档 | X |
| 删除文档 | X |

## 健康指标趋势
| 指标 | 上周 | 本周 | 变化 |
|------|------|------|------|
| Frontmatter 覆盖率 | X% | X% | ↑/↓ |
| 孤立文档占比 | X% | X% | ↑/↓ |
| 总文档数 | X | X | +X |

## 本周活跃模块
（按修改频率排序的模块列表）

## 改进建议
（基于数据自动生成 2-3 条建议）

---
**返回** [[_MOC-知识库总览]]
```

### Step 4: 输出摘要

在终端输出关键指标摘要，方便快速浏览。

## 安全机制

- 只读操作，不修改任何现有文件
- 报告文件写入工作区目录，不影响知识库结构
