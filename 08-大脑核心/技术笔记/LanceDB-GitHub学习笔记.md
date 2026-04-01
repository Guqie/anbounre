---
tags: ['记忆系统', '核心']
date: 2026-03-07
status: 待整理
---

# LanceDB GitHub项目学习笔记

**学习时间：** 2026-02-09 19:48
**来源：** Notion文档中的GitHub链接

---

## 一、lance-graph 项目

**GitHub：** https://github.com/lance-format/lance-graph

### 1.1 项目简介

**Lance Graph** 是一个基于Rust构建的、支持Cypher查询的图查询引擎，具有Python绑定，用于构建高性能、可扩展、无服务器的多模态知识图谱。

**核心特性：**
- 🦀 Rust实现的Cypher查询引擎
- 🐍 Python绑定（PyO3）
- 📊 高性能、可扩展
- 🔍 支持Cypher查询语言
- 🚀 无服务器架构

---

### 1.2 项目结构

**Rust核心：**
- `crates/lance-graph` - Cypher查询引擎（Rust实现）

**Python包：**
- `lance_graph` - Rust查询引擎的Python封装
- `knowledge_graph` - Lance支持的知识图谱CLI、API和工具

---

### 1.3 技术栈

**系统要求：**
- Rust 1.82+
- Python 3.11
- uv（Python包管理器）

---

## 二、核心功能

### 2.1 Cypher查询

**示例代码：**
```python
import pyarrow as pa
from lance_graph import CypherQuery, GraphConfig

# 创建数据表
people = pa.table({
    "person_id": [1, 2, 3, 4],
    "name": ["Alice", "Bob", "Carol", "David"],
    "age": [28, 34, 29, 42],
})

# 配置图
config = (
    GraphConfig.builder()
    .with_node_label("Person", "person_id")
    .build()
)

# 执行Cypher查询
query = (
    CypherQuery("MATCH (p:Person) WHERE p.age > 30 RETURN p.name AS name, p.age AS age")
    .with_config(config)
)
result = query.execute({"Person": people})
print(result.to_pydict())  # {'name': ['Bob', 'David'], 'age': [34, 42]}
```

**关键点：**
- 使用PyArrow表存储数据
- 支持标准Cypher查询语法
- 高性能查询执行

---

### 2.2 知识图谱CLI

**功能：**
- 初始化存储
- 运行Cypher查询
- 通过启发式文本提取引导数据
- FastAPI Web服务

**CLI命令示例：**
```bash
# 初始化存储
uv run knowledge_graph --init

# 列出数据集
uv run knowledge_graph --list-datasets

# 提取预览
uv run knowledge_graph --extract-preview notes.txt

# 执行查询
uv run knowledge_graph "MATCH (n) RETURN n LIMIT 5"

# 使用LLM提取（需要OpenAI API）
export OPENAI_API_KEY=sk-...
uv run knowledge_graph --llm-model gpt-4o-mini --extract-preview notes.txt
```

---

## 三、lance-context 项目

**GitHub：** https://github.com/lance-format/lance-context

### 3.1 项目简介

**Lance Context** 是一个基于Lance构建的多模态、版本化的上下文存储系统，专为AI智能体工作流设计。

**核心价值：**
- 🧠 为AI智能体提供持久化记忆
- 📦 支持文本、二进制数据（图片、Arrow表等）
- 🔍 语义嵌入存储在同一列式表中
- ⏱️ 每次追加产生新版本，支持时间旅行
- 🌿 支持分支和实验

---

### 3.2 为什么需要lance-context？

**核心动机：**

**1. 多模态优先**
- 将文本、图片、结构化数据存储在一起
- 保留原始字节 + 类型化元数据

**2. 版本感知**
- 每次追加创建不可变快照
- 支持时间旅行、分支、审计
- 适合长期运行的智能体

**3. 可搜索的语义**
- 嵌入向量与内容一起管理
- 无需离开数据集即可运行Lance向量搜索

**4. 列式性能**
- 基于Lance文件格式
- 快速分析、压缩、云友好存储

---

### 3.3 核心特性

**1. 统一Schema**
- ContextRecord：智能体消息的统一结构
- 可选嵌入向量和元数据

**2. 自动版本控制**
- 通过Lance清单实现
- 支持checkout(version)

**3. 后台压缩**
- 优化存储和读取性能
- 自动碎片整理

**4. 远程持久化**
- 支持s3:// URI
- AWS环境变量或显式凭证

**5. Python API**
- lance_context.api.Context
- 与Rust实现对齐

---

### 3.4 使用示例

**Python示例：**
```python
from pathlib import Path
from lance_context.api import Context

# 创建上下文
uri = Path("context.lance").as_posix()
ctx = Context.create(uri)

# 添加多模态条目
ctx.add("user", "Where should I travel in spring?")

from PIL import Image
image = Image.new("RGB", (2, 2), color="teal")
ctx.add("assistant", image)

print("Current version:", ctx.version())

# 时间旅行
first_version = ctx.version()
ctx.add("assistant", "Let me fetch suggestions…")
ctx.checkout(first_version)

print("Entries after checkout:", ctx.entries())
```

**S3存储示例：**
```python
ctx = Context.create(
    "s3://my-bucket/context.lance",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region="us-east-1",
    endpoint_url="http://localhost:9000",
    allow_http=True,
)
```

**后台压缩：**
```python
ctx = Context.create(
    "context.lance",
    enable_background_compaction=True,  # 启用自动压缩
    compaction_interval_secs=300,       # 每5分钟检查
    compaction_min_fragments=10,        # 10+碎片时触发
    quiet_hours=[(22, 6)],              # 晚10点-早6点跳过
)

# 手动压缩
metrics = ctx.compact()
print(f"Compaction removed {metrics['fragments_removed']} fragments")
```

---

## 四、LanceDB对我们记忆系统的启示

### 4.1 核心设计理念

**1. 多模态存储**
- 不仅存储文本，还支持图片、结构化数据
- 统一的存储格式
- 保留原始数据 + 元数据

**2. 版本控制**
- 每次修改创建新版本
- 支持时间旅行和回滚
- 可审计的历史记录

**3. 列式存储**
- 基于Lance文件格式
- 高性能查询
- 云友好存储

**4. 语义搜索**
- 嵌入向量与内容一起存储
- 支持向量搜索
- 混合检索（关键词 + 语义）

---

### 4.2 与我们系统的对比

**相似之处：**
- ✅ 持久化记忆存储
- ✅ 支持语义搜索
- ✅ 版本控制理念

**差异之处：**
- 📝 LanceDB：列式存储，高性能
- 📝 我们：Markdown文件，人类可读
- 📝 LanceDB：多模态支持
- 📝 我们：主要是文本

---

### 4.3 可借鉴的设计

**1. 版本控制机制**
```python
# LanceDB的版本控制
ctx.version()  # 获取当前版本
ctx.checkout(version)  # 回滚到指定版本
```

**应用到我们的系统：**
- 使用Git进行版本控制
- 每次重要更新创建commit
- 支持回滚到历史状态

**2. 后台压缩机制**
```python
# LanceDB的自动压缩
enable_background_compaction=True
compaction_interval_secs=300
```

**应用到我们的系统：**
- 定期整理记忆文件
- 归档旧的日志
- 压缩重复内容

**3. 统一Schema**
```python
# LanceDB的ContextRecord
{
    "id": "run-1-1",
    "role": "user",
    "content_type": "text/plain",
    "text_payload": "hello world",
    "embedding": [...]
}
```

**应用到我们的系统：**
- 定义统一的记忆条目格式
- 包含元数据（时间、类型、优先级）
- 支持嵌入向量

---

### 4.4 实施建议

**短期（本周）：**
1. ✅ 定义统一的记忆条目格式
2. ✅ 创建SQLite数据库存储元数据
3. ✅ 实现基础版本控制（Git）

**中期（本月）：**
1. ⏳ 集成向量搜索（考虑使用LanceDB或Chroma）
2. ⏳ 实现后台压缩机制
3. ⏳ 支持多模态存储（图片、文件）

**长期（持续）：**
1. ⏳ 迁移到Lance格式（可选）
2. ⏳ 实现完整的版本控制系统
3. ⏳ 优化查询性能

---

## 五、总结

### 5.1 关键收获

**1. lance-graph**
- Cypher查询引擎
- 知识图谱构建
- 高性能图查询

**2. lance-context**
- 多模态上下文存储
- 版本控制
- 智能体记忆管理

**3. 设计理念**
- 列式存储 + 版本控制
- 多模态 + 语义搜索
- 高性能 + 云友好

### 5.2 对我们的价值

**立即可用：**
- 统一的记忆条目格式
- 版本控制机制
- 后台压缩策略

**中期规划：**
- 集成向量搜索
- 多模态支持
- 性能优化

**长期愿景：**
- 考虑迁移到Lance格式
- 构建知识图谱
- 实现完整的智能体记忆系统

---

**学习完成时间：** 2026-02-09 19:52
**下一步：** 基于学习成果，更新记忆系统优化规划v3.0

