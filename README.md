# Code LLM Wiki

一套以 **Skill / Prompt** 驱动的代码知识沉淀工作流，面向由多个独立进程/服务仓库组成的工程系统。

核心目标：从 Superproject、Git Submodules、源码和现有工程文档中提取有证据支撑的知识，以 Process 为基本单元组织，再整合成 System 级架构知识，最终沉淀到独立 Wiki 仓库。

## 当前设计范围

- **知识模型**：Process 为核心，System 为跨进程知识整合层。
- **仓库关系**：Repository 与 Process 为多对多关系；Process/Profile 映射独立记录。
- **平台范围**：QNX、Android、Linux（TBOX）。
- **平台建模**：通过 Platform Profile 区分平台共性和特有实现。
- **源码证据**：重要结论拆分为 Claim，并关联 Evidence、repository、full commit 和 locator。
- **增量更新**：通过 Page-Source Map 反向定位受源码变化影响的页面和 Claim。
- **构建关系**：可选使用 CMake Graphviz DOT 辅助分析 Target 级依赖。
- **AST**：第一阶段暂不引入。
- **Ingest**：Repository Discovery → bounded Analysis Tasks → Task Reports / Checkpoint → Process Integration；避免全仓库源码一次性进入模型上下文。
- **上下文管理**：任务范围、逻辑单元级持久化、Sequential Session Handoff/Resume 与最小 Context Pack 均由 Skill/Prompt 规范；不依赖 Subagent 或独立运行时。
- **质量门禁**：Lint → 自动委派独立 Review Subagent → Human Review → 显式授权发布。
- **状态管理**：Claim、Evidence、Change Set、Review、Human Decision 和 Publication 状态分开管理。
- **输出语言**：Skill 指令以英文维护；Wiki 和报告默认简体中文。
- **知识维护**：目标 Wiki 自带 `AGENTS.md` 维护入口、持续同步的 `index.md` 和追加式 `log.md`；普通查询默认只读，用户要求保存的问答成果进入候选更新与评审。

## 工作流

```text
Init
  -> Ingest (per Repository / Process)
  -> Integrate (System-level)
  -> Lint
  -> Automatic Independent Review Subagent
  -> Human Approval
  -> Explicit Publication
  -> Incremental Update
```

- `init`：盘点 Superproject、Submodules、AGENTS.md、commit 和候选映射。
- `ingest`：分析单个 Repository / Process，生成 Claim-Evidence 对应的知识页面。
- `integrate`：整合多个 Process，形成 System 级架构知识。
- `query`：从索引定位已发布知识，显式区分推断、未知和过期内容；需要保存答案时转入 `update`。
- `update`：根据源码变化和 Page-Source Map，或明确要求保存的查询发现，生成候选更新；同步页面链接和索引。
- `review`：由入口 Skill 自动委派独立 Subagent，在新上下文中复核知识结论、证据和关系；不支持手动新建会话的回退流程。
- `lint`：检查结构、链接、证据、映射、状态和一致性。

## 仓库结构

- `SKILL.md`：入口 Skill 与工作流路由。
- `skills/`：7 个独立工作流 Skill。
- `docs/`：架构、Schema、Claim/Evidence、状态机、失败处理、质量门禁、人工审批和 Skill 合约。
- `references/`：知识模板、Manifest、Page-Source Map、各类报告和决策记录模板。
- `examples/`：合成示例材料。
- `tests/recovery_fixture.py`：生成和检查恢复演练的数据，不执行 Wiki 工作流；见 [合成恢复验证](examples/recovery-validation.md)。

## 核心约束

- 不按目录结构机械划分 Process。
- Repository ↔ Process 为多对多；Profile 支持必须落到 Process 级别。
- 区分 Build Dependency、Runtime Dependency、IPC 和 Startup Ordering。
- CMake DOT 只能作为构建关系证据，不能据此推断运行时关系。
- 平台共性必须有证据支撑；未知内容标记为 Unknown。
- 重要 Claim 必须有逐条 Claim-Evidence 映射。
- 未通过 Lint、独立 Review、人工批准并显式发布的候选内容不得作为正式知识。
- 人工审批绑定精确 Diff、Wiki revision 和相关 Source Manifest/source revisions；内容变化使审批失效。
- 增量更新不得覆盖未经确认的人工修订。
- 失败、跳过、不可访问和未执行的检查必须显式报告，不能伪装成 PASS。

## 使用入口与生成物

保留本仓库的完整目录，让具备文件、Git 和隔离子 Agent 能力的 Coding Agent 读取根目录 `SKILL.md`，并提供源码工作区、独立 Wiki Git 仓库和首轮分析范围。工作流引用路径以本 Skill 仓库根目录为基准。当前没有独立 CLI 或后台服务。

`init` 在目标 Wiki 仓库生成维护入口和骨架：

```text
AGENTS.md                    # 本地维护规则、路径和完整 Skill 的版本化定位信息
wiki/
  index.md                   # 页面链接、摘要、范围及发布状态
  log.md                     # 已发生操作的追加式时间线
  system/ processes/         # 系统与进程知识
  interfaces/ workflows/     # 接口与跨进程流程
  _meta/                     # 源码清单、结论/证据、变更与评审记录
```

后续 Agent 从目标仓库的 `AGENTS.md` 开始，查询先读索引。用户要求“把这个分析保存到 Wiki”时，先复用已有页面与原始证据，再生成候选变更并通过原有检查、评审和发布流程。源码版本不变也可能产生新的知识变更。

普通查询默认不写文件，也不写日志；可在目标 Wiki 明确启用仅记录查询日志的策略。检查与评审后产生的事件由主 Agent 记录在冻结快照之外，不得修改已经评审的候选内容。详情见 [Wiki 维护规则](docs/wiki-maintenance.md)。

这套结构采用 [Karpathy 的 LLM Wiki 思路](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，并针对代码工程增加证据、版本和评审约束。原文是可按领域调整的模式说明，不是固定目录标准；本项目不宣称通过官方符合性认证。

## 设计规范索引

- [Architecture](docs/architecture.md)
- [Context-Bounded Ingestion and Session Handoff](docs/context-management.md)
- [Wiki Schema](docs/wiki-schema.md)
- [Wiki Navigation, Logging, and Query Capture](docs/wiki-maintenance.md)
- [Snapshot Binding and Cross-session Recovery](docs/snapshot-binding.md)
- [Publication Progress and Safe Retry](docs/publication-recovery.md)
- [Claim / Evidence / Page-Source Map](docs/claim-evidence-model.md)
- [Workflow State Model](docs/state-machine.md)
- [Failure Handling](docs/failure-handling.md)
- [Skill Contracts](docs/skill-contracts.md)
- [Source Evidence](docs/source-evidence.md)
- [Strict Quality Gate](docs/quality-gate.md)
- [Automatic Independent Review Execution](docs/independent-review-execution.md)
- [Human Review and Publication](docs/human-review.md)
- [Language Policy](docs/language-policy.md)
- [Architecture Decisions](docs/decisions.md)

## Report and template index

- Claim / Evidence: `references/claim-template.md`
- Analysis Task: `references/analysis-task-template.md`
- Ingestion Checkpoint: `references/checkpoint-template.md`
- Session Handoff: `references/session-handoff-template.md`
- Session Context Pack: `references/context-pack-template.md`
- Change Set: `references/change-set-template.md`
- Platform Profile: `references/platform-profile-template.md`
- Architecture Decision: `references/architecture-decision-template.md`
- Source Manifest: `references/source-manifest-template.md`
- Page-Source Map: `references/page-source-map-template.md`
- Repository / Process / System / Interface / Workflow / Platform Profile: `references/*-template.md`
- Init / Ingestion / Integration / Update / Lint / Review: `references/*-report-template.md`
- Automatic Review Subagent Task: `references/review-agent-task-template.md`
- Human Review Summary: `references/human-review-summary-template.md`
- Human Decision: `references/human-decision-template.md`
- Destination Wiki Entry: `references/wiki-agents-template.md`
- Content Index / Operation Log: `references/wiki-index-template.md`, `references/wiki-log-template.md`
- Query Capture: `references/query-capture-template.md`
- Snapshot Binding: `references/snapshot-binding-template.md`
- Publication Plan / Progress and Authorization: `references/publication-plan-template.md`, `references/publication-progress-template.md`

The current design defines a context-bounded, resumable Skill/Prompt workflow and its design contracts. It does not claim that a real business repository has passed an end-to-end POC.
