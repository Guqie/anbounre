# Memory 权限模型与写回治理规范

> **版本**：v1.0
> **维护者**：哈雷酱 + 小顾姥爷
> **最后更新**：2026-03-08
> **相关文档**：[系统架构总览](../architecture/README.md)｜[Subagent 架构](01-subagent-architecture.md)｜[Subagent 宪法](03-subagent-constitution.md)

---

## 设计原则

### 分层原则

所有记忆都必须显式分层，禁止将所有历史内容视为同一类上下文。

### 最小召回原则

默认只召回完成当前任务所需的最小记忆集合，禁止"大而全"地装入所有相关历史。

### 预算感知原则

记忆召回、压缩、写回、反思都应计入预算，不应被视为零成本操作。

### 写回门槛原则

写回必须经过质量、价值、权限、成本四重判断，不得将"模型生成过的结果"直接等同于"值得长期记住"。

### 压缩优先原则

在多数场景下，应优先使用摘要、压缩包、提要结构和缓存结果，而非频繁读取原始长文本。

### 审计可回滚原则

所有重要写回都必须可审计、可追踪、可撤销、可版本化。

### 污染防控原则

系统应将防止低质量、偶发性、过时性、冲突性内容进入长期记忆视为最高优先级治理目标之一。

---

## 记忆分层模型

系统记忆分为六层：

### L1：瞬时工作上下文（Ephemeral Working Context）

**定义**：当前轮对话、当前 session 的即时输入输出与运行时中间状态。

**生命周期**：最短，可频繁变化，不默认进入长期记忆，可直接用于 agent 协作。

**适用内容**：当前任务输入、中间推理产物摘要、当前 session 临时工具结果、当前预算与路由状态。

### L2：工作记忆（Working Memory）

**定义**：围绕当前任务或当前短期工作流形成的阶段性上下文压缩包。

**生命周期**：中短，可跨几个相关 session 复用，适合存放阶段性共识。

**适用内容**：当前研究任务的进展摘要、当前方案讨论的临时结论、最近几轮对话形成的上下文包。

### L3：项目记忆（Project Memory）

**定义**：围绕主题、项目、任务流、长期目标积累的持续记忆。

**生命周期**：较长，跨会话复用的重要层，需要明确主题边界、需要版本和时效标记。

**适用内容**：项目背景、当前阶段目标、关键里程碑、项目知识地图、核心术语与约定。

### L4：用户记忆（User Memory）

**定义**：与长期协作方式、偏好、表达习惯、稳定需求相关的用户侧记忆。

**生命周期**：敏感度高，应严格控制读写，必须可审计，不应混入短期噪声。

**适用内容**：偏好的输出结构、风格偏好、长期工作方式偏好、稳定关注主题。

### L5：决策记忆（Decision Memory）

**定义**：历史关键判断、选择、假设、取舍理由与边界条件的结构化存档。

**生命周期**：高价值，高复用，必须保留理由与边界，不能只存结论不存依据。

**适用内容**：架构选型及原因、取舍判断和 rejected alternatives、假设条件与失效条件、关键策略结论。

### L6：角色/演进记忆（Role & Evolution Memory）

**定义**：系统自身长期能力变化、规则演进、角色基准与升级轨迹。

**生命周期**：高门槛，高敏感，只能由少数主体读写，需强审计和版本控制。

**适用内容**：人格核长期调整记录、方法包升级记录、输出协议核心变化、演进规则变更记录。

---

## 记忆对象模型

### MemoryRecord 最小字段

- memory_id, memory_type, title
- content_summary（默认供低成本召回使用）
- content_ref（指向原始文档或完整存储位置）
- source_session_id, source_agent, source_type
- created_at, updated_at
- freshness_tag: stable / recent / volatile / archived / deprecated
- confidence, importance_score
- privacy_level: public_to_system / restricted_agent / high_sensitivity
- project_scope, user_scope, recall_tags
- writeback_level, version, supersedes, audit_ref

---

## 召回策略设计

### 召回流水线（5 步）

1. **Scope 定位**：判断需要哪一类记忆
2. **候选召回**：从索引、缓存、最近会话中获取候选
3. **价值裁剪**：按任务相关性、预算、时效、敏感度做筛选
4. **压缩整理**：生成 memory context 包
5. **交付下游**：提供给 Copilot 或具体 agent

### 召回优先级

1. 当前 session 的工作记忆压缩包
2. 最近相关项目记忆摘要
3. 相关决策记忆
4. 用户偏好摘要
5. 原始长文档或原始记录

> **默认先召回摘要和压缩包，再决定是否向原始内容下钻。**

### 召回模式

| 模式 | 适用场景 | 特征 |
|------|---------|------|
| **轻量召回** | chat / write | 只取工作记忆 + 用户风格偏好 + 必要项目摘要，禁止加载大量原始文档 |
| **研究召回** | research | 取项目记忆摘要 + 相关决策记忆，必要时下钻部分原始资料 |
| **判断召回** | decision | 取研究摘要 + 历史决策记忆 + 必要项目背景，保证理由与边界信息完整 |
| **演进召回** | reflect / evolve | 取 reflection summary + 历史 proposal + 角色/演进记忆摘要，禁止大规模无差别读取 |

---

## 压缩与上下文封装策略

### Compression-first 原则

Memory Agent 应优先生成以下结构：

- task summary pack
- project memory digest
- decision rationale digest
- user preference digest
- unresolved issues list

### MemoryContext 结构

```python
@dataclass
class MemoryContext:
    context_id: str
    session_id: str
    objective: str
    included_memory_types: List[str]
    summary_blocks: List[Block]
    key_facts: List[str]
    key_constraints: List[str]
    prior_decisions: List[Decision]
    user_preferences: List[Preference]
    unresolved_items: List[str]
    source_refs: List[str]
    freshness_notes: str
    confidence: float
    token_estimate: int
```

### 压缩质量要求

压缩内容必须：

- 保留结论与依据的基本对应关系
- 保留时效性标记
- 保留不确定性
- 保留 source_refs
- 不擅自消解历史冲突

---

## 写回治理总流程

写回不是"保存内容"，而是"治理动作"。建议将写回设计成 7 步：

1. 候选生成
2. 价值评估
3. 权限检查
4. 成本评估
5. Proposal 创建
6. 审批 / 自动批准 / 拒绝
7. 提交、版本化、审计与可回滚记录

### 写回候选判断维度

至少应检查：relevance、stability、novelty、evidence、risk、cost、authority。

---

## Writeback Proposal 状态机

### 状态定义

- Drafted → Evaluated → PendingApproval / AutoApproved → Committed
- Drafted → Evaluated → Rejected
- Committed → RolledBack
- Rejected / Committed / RolledBack → Archived

### 自动批准条件

仅在满足以下条件时允许 AutoApproved：

- Level A 写回
- evidence 明确
- novelty 适中
- 风险低
- 成本低
- 无冲突记录

---

## 冲突检测与版本治理

### 冲突类型

- **内容冲突**：新结论与旧结论不一致
- **时效冲突**：旧内容已过时但未标记
- **范围冲突**：写错项目或写错用户范围
- **权限冲突**：无权主体尝试写高等级内容
- **语义重复**：内容几乎重复但占用新条目
- **级别冲突**：低等级内容尝试覆盖高等级记忆

### 冲突处理策略

- 轻微重复：合并或 supersede
- 时效替换：新版本 supersede 旧版本
- 重大冲突：拒绝自动提交，升级审批
- 权限冲突：直接拒绝并审计
- 无法判断：进入 PendingApproval

---

## 预算与成本治理

### 写回与预算联动规则

- Level A 写回可在低预算下保留最小摘要版
- Level B 写回预算不足时，可只生成 proposal 不立即提交
- Level C 写回预算不足时，应直接延后，不得草率推进
- Reflection / Evolution 的相关写回默认后置于主任务完成之后

---

## 污染防控策略

### 典型污染来源

1. 单次偶发偏好被写成长期用户记忆
2. 未验证的研究结论进入项目记忆
3. 低置信度判断进入决策记忆
4. 过时信息覆盖新信息
5. 写作层润色文本误被当成事实源
6. Reflection 的噪声观察误入演进记忆
7. 错误用户范围或项目范围写入

### 防控规则

- 低置信度内容默认不得写长期层
- 写作层输出原则上不作为事实源
- 用户偏好至少应有稳定重复出现或显式确认
- 决策记忆必须附理由与边界
- 演进记忆必须依赖多次 reflection 汇总
- 所有长期写回都必须进行冲突与范围检查

---

## 附录：目录结构

```
memory/
  models/
    memory_record.py
    proposal.py
    context_pack.py
  policies/
    access_policy.py
    recall_policy.py
    compression_policy.py
    writeback_policy.py
    conflict_policy.py
    rollback_policy.py
  registry/
    memory_registry.py
    audit_log.py
  recall/
    recall_pipeline.py
    candidate_ranker.py
    context_compressor.py
  writeback/
    proposal_engine.py
    commit_engine.py
    rollback_engine.py
  cache/
    l1_cache.py
    l2_cache.py
    l3_cache.py
  tests/
    test_access_control.py
    test_recall_budget.py
    test_proposal_state_machine.py
    test_conflict_detection.py
    test_contamination_prevention.py
```

---

**维护者**：哈雷酱 + 小顾姥爷
**最后更新**：2026-03-08
**版本**：v1.0
