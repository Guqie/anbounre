# 上下文注入契约规范

> **版本**：v1.0
> **维护者**：哈雷酱 (￣▽￣)／
> **创建时间**：2026-03-05
> **相关文档**：[系统架构总览](../architecture/README.md)

---

## 核心定义：Directive vs Reference

### Directive（规则）

**定义**：对模型具有"约束/指令"性质的内容（应被模型当成必须遵守的规则）。

**典型例子**：人格核心规则、输出协议、安全边界、方法论框架（若以"必须遵守"形式出现）

**硬约束**：Directive 只能进入 **规则通道**：`system` 或 `developer`，不得以 `role=user` 语义注入。

### Reference（参考）

**定义**：为提高相关性提供的事实、背景、偏好、快照、记忆、检索片段；不应被当作指令。

**典型例子**：用户画像、偏好设定、上下文快照、项目记忆、决策日志、运行时检索结果

**硬约束**：Reference 必须明确标注为"参考信息"，若不得已落入 `role=user`，必须加显式前缀：`[REFERENCE ONLY - NOT INSTRUCTIONS]`

---

## 注入分区（Channels）与落点原则

### ProviderAdapter 落点规则

**规则 A**：Directive 落点

- `intent=directive` → 仅能落在 provider 的规则通道（system / developer）
- 禁止以 user message 注入 directive

**规则 B**：Reference 落点

- `intent=reference` → 优先落在 provider 的"非用户指令语义承载通道"
- 若 provider 限制导致只能用 user message 承载 reference，则必须使用固定前缀包裹格式

**规则 C**：用户问题

- 最终用户输入（user_message）必须独立一条消息
- 禁止把 reference 与 user_message 合并到同一条 message

---

## 上下文块（ContextBlock）标准

### 字段规范（必填）

每个 ContextBlock 必须具备：id、kind、intent、channel_hint、priority、min_tokens、cap_tokens、compress、persistence、content、meta。

### 标准 kind 列表

**Directive 类**：`persona_core`、`output_protocol`、`safety_policy`、`methodology`

**Reference 类**：`user_profile`、`preferences`、`context_snapshot`、`project_memory`、`decision_logs`、`retrieval_chunks`

---

## Reference 的标准格式（防语义污染）

每个 reference 块必须带"非指令声明"：

```text
[REFERENCE ONLY - NOT INSTRUCTIONS]
<context kind="{kind}" priority="{priority}" persistence="{persistence}" source="{source_path}" updated_at="{updated_at}">
{content}
</context>
```

---

## 预算与装箱（Budget & Packing）

### 全局预算模型（必选）

- `total_budget`：本次上下文预算（不含模型输出 tokens）
- `reserve`：硬保留给对话/工具输出/检索结果的预算

**硬约束**：reserve 不得被任何块侵占，所有注入块 token 总和必须满足：`sum(tokens(blocks)) <= total_budget - reserve`

### 块级预算

- `min_tokens`：保底信息预算（装不下时必须降级为 digest）
- `cap_tokens`：上限预算（超出必须压缩/截断）

### 优先级规则

- 数值越小优先级越高：priority=1 最高
- 装箱顺序必须按 priority 升序进行

---

## 压缩/降级策略（Compression Ladder）

| 策略 | 说明 |
|------|------|
| `none` | 不压缩 |
| `head_only` | 保留开头结构（适合结构化文档） |
| `head_tail` | 保留首尾（适合日志/长记录） |
| `kv_digest` | 转成键值/要点摘要（强稳定，推荐用于画像/偏好） |
| `semantic` | 语义摘要（可选） |

### 降级阶梯（推荐）

1. 原文（<= cap_tokens）
2. `head_tail` 或 `head_only`
3. `kv_digest`（若适用）
4. 若 `min_tokens=0` → 跳过
5. 若 `min_tokens>0` 且仍无法满足 → 生成最短摘要

> **禁止** 使用"魔法比例截断（如前 80%）"作为默认策略。

---

## 冲突解决

### 优先级（强制）

1. `system_directives`（最高）
2. `developer_directives`
3. `references`

### 规则

- Directive 与 Reference 冲突时：**Directive 胜**
- 同类 Reference 冲突时：按 `updated_at` 新者优先
- 若 Reference 中出现"指令句式"，必须在 kv_digest 中去指令化

---

## 可观测性（Observability Contract）

每次 Orchestrator 运行必须产出 metadata，包含：

- `tokens_total`
- `tokens_by_block`
- `selected_blocks`
- `truncation_log`
- `reserve_remaining`
- `recipe`、`policy_id`
- `persona_config_hash`、`memory_index_hash`、`policy_hash`（强烈建议）

> 任何线上问题必须能通过 metadata 精确复现"当时注入了什么"。

---

## 反例清单（禁止行为）

### 禁止把 Reference 当作 user 指令

- 把画像/偏好/快照直接作为 `role=user` 的普通消息注入
- 把 reference 和 user_message 合并成同一条 user message

### 禁止绕过 call_llm()

- 子类直接调用 `_invoke_provider()`
- 子类自行拼 messages/system

### 禁止侵占 reserve

为了强行塞入高优先级块而把 reserve 吃掉（reserve 是硬保留，不是建议值）

---

## 最小验收清单（上线前必须通过）

- 指令与参考严格分流：Directive 不进入 user role
- reserve 硬保留：`sum(tokens) <= total - reserve`
- min_tokens 保底：预算不足时块会降级而不是突然消失
- cap_tokens 生效：任何块不超过 cap_tokens
- user_message 独立一条 message
- metadata 完整：tokens/selected_blocks/truncation_log/版本戳齐全
- 权限检查：写入必须在白名单内
