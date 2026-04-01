---
tags: ['AI', '技术文档']
date: 2026-03-07
status: 待整理
---

# [CLAUDE.md](http://claude.md/) 大师课：从入门到精通

[claude.md](http://claude.md) 是 Claude 的大脑，今天结构化写一下如何更好的使用 [claude.md](http://claude.md)

1. [claude.md](http://claude.md) 解决的问题

每一次新增 Claude Code 会话时，它对你的项目一无所知：

- 它不知道你的技术栈
- 它不知道你的文件夹结构
- 它不知道你喜欢用 Tab 还是空格，也不知道你的团队使用的分支命名规范

所以你应该每次都解释你的项目，很费时间

[claude.md](http://claude.md) 是一个 Markdown 文件，它为 Claude 提供关于你项目的持久记忆

只需创建一次，每个会话开始时 Claude 都会自动读取它

1. 什么是 [claude.md](http://claude.md)

[claude.md](http://claude.md) 不是文档文件，而是配置文件，它会成为 Claude 系统提示词的一部分

当你将指令放入 [claude.md](http://claude.md) 时，Claude 会比对你在聊天框中输入的内容更加严格地遵循这些指令

这就是为什么一个设计良好的 [claude.md](http://claude.md) 能够改变你的整个工作流程，并为每次对话设定操作边界

1. 为什么 Claude 会忽略你的 [CLAUDE.md](http://claude.md/)？

Claude Code 在你的 [CLAUDE.md](http://claude.md/) 外包裹了一个系统提醒，告诉 Claude 忽略不相关的内容：

<system-reminder> IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task. </system-reminder>

这意味着如果你在 [CLAUDE.md](http://claude.md/) 中塞入不具有普遍适用性的指令，Claude 将会忽略它们

1. 撰写 [claude.md](http://claude.md) 的普遍原则

- **项目记忆**——Claude 在会话之间记住你的设置
- **操作边界**——Claude 不会打破的规则
- **上下文引导**——Claude 开始时就有所了解，而不是一片空白

理解这种心智模型后，你就不会再把 [CLAUDE.md](http://CLAUDE.md) 当作 README，这是你在 Claude Code 中拥有的最重要的配置点

精简，普遍适用是写 [claude.md](http://claude.md) 的重要原则，千万不要把太多的项目细节放进去，这些信息没有用，而且会影响其他有用的信息

1. **[CLAUDE.md](http://CLAUDE.md) 的层级结构**

[CLAUDE.md](http://claude.md/) 文件可以存在于多个位置，并且 Claude 会按照特定顺序读取它们

全局（Global）

- **位置**：`~/.claude/CLAUDE.md`
- **加载时机**：每次会话，始终加载
- **使用场景**：个人偏好设置、通用规则

项目（Project）

- **位置**：`/project/CLAUDE.md`
- **加载时机**：当你在该目录下运行 Claude 时加载
- **使用场景**：项目架构、团队规范

嵌套（Nested）

- **位置**：`/project/src/CLAUDE.md`
- **加载时机**：当 Claude 读取该目录下的文件时加载
- **使用场景**：特定目录的规则或模式

1. monorepo 的设置方式

```jsx
my-monorepo/
├── CLAUDE.md                    # 整个仓库的规则
├── apps/
│   ├── web/
│   │   └── CLAUDE.md            # 前端特定规则
│   └── api/
│       └── CLAUDE.md            # 后端特定规则
├── packages/
│   └── shared/
│       └── CLAUDE.md            # 共享库规则
└── tests/
    └── CLAUDE.md                # 测试规范
```

嵌套文件只有在 Claude 访问那些目录中的文件时才会加载。这使你的主要上下文保持精简，直到 Claude 需要这些专业知识

文件命名选项：

- `CLAUDE.md`——标准名称，提交到 git，与团队共享
- `CLAUDE.local.md`——加入 `.gitignore`，用于个人偏好，不推送到仓库

1. 优秀的 [CLAUDE.md](http://claude.md/) 的构成

- **WHAT**——技术栈、项目结构、关键文件
- **WHY**——项目的目的，每个部分的作用
- **HOW**——运行命令、工作流程和需要遵守的约定

一个例子：

````jsx
## 关于本项目

基于 FastAPI 的 REST API，用于用户认证和用户资料管理。  
使用 SQLAlchemy 进行数据库操作，使用 Pydantic 进行数据验证。

## 关键目录

- `app/models/` —— 数据库模型
- `app/api/` —— 路由处理器
- `app/core/` —— 配置与工具函数
- `tests/` —— 测试文件（fixture 位于 `tests/conftest.py`）

## 常用命令

```bash
uvicorn app.main:app --reload  # 开发服务器
pytest tests/ -v               # 运行测试
alembic upgrade head           # 执行数据库迁移
````

1. [claude.md](http://claude.md) 的限制

[claude.md](http://claude.md) 最多容纳 150-200 条指令，超过这个数量，效果会变差

一定要包含的部分：

项目简介，技术栈，核心命令，目录架构

按需要纳入的部分：

命名规范，commit 规范，测试要求，部署流程

不要写入的部分：

api key 等敏感信息，linter 等详细的代码规范，特性要求，还有其他一切 cladue 可以通过阅读代码而知道的信息

1. 特定的指令可以单独存放，做好索引即可

```jsx
project/
├── CLAUDE.md                        # Core instructions only
└── agent_docs/
    ├── building_the_project.md
    ├── running_tests.md
    ├── code_conventions.md
    ├── database_schema.md
    └── deployment_process.md
```

索引：

```jsx
## 附加文档

在开始具体任务之前，请阅读相关文档：

- 构建（Building）：`agent_docs/building_the_project.md`
- 测试（Testing）：`agent_docs/running_tests.md`
- 数据库相关工作（Database work）：`agent_docs/database_schema.md`
- 部署（Deployment）：`agent_docs/deployment_process.md`

只阅读与你当前任务相关的内容。
```

进阶

1. 复杂项目建立索引

建立索引文件

```jsx
# general_index.md

## /src/api/
- `auth.py` —— 认证相关接口，JWT 处理
- `users.py` —— 用户的增删改查（CRUD）操作
- `products.py` —— 商品目录相关接口

## /src/models/
- `user.py` —— 用户模型，以及与订单的关联关系
- `product.py` —— 商品模型，库存跟踪

## /src/utils/
- `validators.py` —— 输入校验辅助函数
- `formatters.py` —— 响应格式化工具
```

在 [claude.md](http://claude.md) 里面引用

```jsx
## 导航

我已提供索引文件以帮助你进行代码导航：

- `general_index.md` —— 各模块的文件说明
- `detailed_index.md` —— 函数签名与文档字符串（docstring）

这些索引文件可能是最新的，也可能不是。在需要时，请通过查看实际文件进行核实。
```

1. 将 [claude.md](http://claude.md) 模块化设计

```jsx
## 开发命令（Development Commands）
<!-- 构建、测试、运行说明 -->

## 代码规范（Code Standards）
<!-- 适用于整个项目的编码约定 -->

## 工作流程（Workflow Procedures）
<!-- 完成常见任务的步骤说明 -->

## 文件边界（File Boundaries）
<!-- Claude 可以和不可以修改的内容范围 -->

## 工具集成（Tool Integration）
<!-- MCP 服务器、自定义命令等 -->
```

1. 复杂任务使用工作流，避免 claude 未了解全局情况而直接上手改代码

```jsx
### 新增一个 API 接口

1. 检查 `src/api/` 中是否已存在类似接口  
2. 如果需要新的数据类型，在 `src/schemas/` 中创建对应的 schema  
3. 在合适的路由文件中实现该接口  
4. 在 `tests/api/` 中添加测试用例  
5. 更新 API 文档  
6. 在提交前运行完整的测试套件  

---

### 数据库 Schema 变更

1. 描述变更内容及其必要性  
2. 创建迁移文件：  
   `alembic revision --autogenerate -m "描述信息"`  
3. 审查自动生成的迁移文件  
4. 测试迁移：  
   `alembic upgrade head`  
5. 测试回滚：  
   `alembic downgrade -1`  
6. 更新相关的模型（models）和 schema
```

1. 按照开发/部署，或者前端/后端来区分维护 [claude.md](http://claude.md)

```
project/
├── CLAUDE.md                 # 当前生效的配置文件
├── .claude/
│   ├── CLAUDE.development.md # 开发阶段侧重点配置
│   ├── CLAUDE.deployment.md  # 部署阶段侧重点配置
│   └── CLAUDE.debugging.md   # 调试阶段侧重点配置
```

1. 如果你使用 mcp，要说明

```
## MCP 集成（MCP Integrations）

### Slack MCP
- 仅向 #dev-notifications 频道发送消息  
- 用于部署通知和构建失败通知  
- 不用于单个 PR 的更新通知  
- 每小时限制发送 10 条消息  

### Database MCP
- 对生产环境只读副本拥有只读访问权限  
- 仅用于数据探索，绝不可进行写入操作  
- 在可能的情况下，优先使用该 MCP，而不是直接执行原始 SQL  
```

1. 使用 sub-agent

```
## 子代理指南（Subagent Guidelines）

在将任务委托给子代理时：

- 安全审查：使用全新的子代理，不要携带实现阶段的上下文信息  
- 代码探索：子代理应首先阅读 `general_index.md`  
- 文档相关任务：子代理可以自由访问 `docs/` 目录  
```

总结

- [CLAUDE.md](http://claude.md/) 是配置文件，而不是项目文档
- Claude 会将其视为系统级规则，其优先级高于普通提示词
- 少即是多 —— 如果内容超过 100–150 条指令，说明你做得太多了
- 使用分层结构：全局（global）→ 项目（project）→ 嵌套（nested）
- 渐进式披露优于臃肿的文件结构
- 使用 # 持续把新的规则迭代进入 [claude.md](http://claude.md)