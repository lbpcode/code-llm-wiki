# Code LLM Wiki

一套以 **Skill / Prompt** 驱动的代码知识沉淀工作流，面向由多个独立进程/服务仓库组成的工程系统。

核心目标：从 Superproject、Git Submodules、源码和现有工程文档中提取有证据支撑的知识，以 Process 为基本单元组织，再整合成 System 级架构知识，最终沉淀到独立 Wiki 仓库。

## v0.1.0 设计范围

- **知识模型**：Process 为核心，System 为跨进程知识整合层。
- **仓库关系**：Repository 与 Process 为多对多关系；Process/Profile 映射独立记录。
- **平台范围**：QNX、Android、Linux（TBOX）。
- **平台建模**：通过 Platform Profile 区分平台共性和特有实现。
- **源码证据**：重要结论拆分为 Claim，并关联 Evidence、repository、full commit 和 locator。
- **增量更新**：通过 Page-Source Map 反向定位受源码变化影响的页面和 Claim。
- **构建关系**：可选使用 CMake Graphviz DOT 辅助分析 Target 级依赖。
- **AST**：第一阶段暂不引入。
- **质量门禁**：Lint → 独立 LLM Review → Human Review → 显式授权发布。
- **状态管理**：Claim、Evidence、Change Set、Review、Human Decision 和 Publication 状态分开管理。
- **输出语言**：Skill 指令以英文维护；Wiki 和报告默认简体中文。

## 工作流

```text
Init
  -> Ingest (per Repository / Process)
  -> Integrate (System-level)
  -> Lint
  -> Independent Review
  -> Human Approval
  -> Explicit Publication
  -> Incremental Update
```

- `init`：盘点 Superproject、Submodules、AGENTS.md、commit 和候选映射。
- `ingest`：分析单个 Repository / Process，生成 Claim-Evidence 对应的知识页面。
- `integrate`：整合多个 Process，形成 System 级架构知识。
- `query`：默认只查询已发布知识，显式区分推断、未知和过期内容。
- `update`：根据源码变化和 Page-Source Map 生成候选更新。
- `review`：在独立上下文中复核知识结论、证据和关系。
- `lint`：检查结构、链接、证据、映射、状态和一致性。

## 仓库结构

- `SKILL.md`：入口 Skill 与工作流路由。
- `skills/`：7 个独立工作流 Skill。
- `docs/`：架构、Schema、Claim/Evidence、状态机、失败处理、质量门禁、人工审批和 Skill 合约。
- `references/`：知识模板、Manifest、Page-Source Map、各类报告和决策记录模板。
- `examples/`：合成示例材料。

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

## 设计规范索引

- [Architecture](docs/architecture.md)
- [Wiki Schema](docs/wiki-schema.md)
- [Claim / Evidence / Page-Source Map](docs/claim-evidence-model.md)
- [Workflow State Model](docs/state-machine.md)
- [Failure Handling](docs/failure-handling.md)
- [Skill Contracts](docs/skill-contracts.md)
- [Source Evidence](docs/source-evidence.md)
- [Strict Quality Gate](docs/quality-gate.md)
- [Human Review and Publication](docs/human-review.md)
- [Language Policy](docs/language-policy.md)
- [Architecture Decisions](docs/decisions.md)

## Report and template index

- Claim / Evidence: `references/claim-template.md`
- Change Set: `references/change-set-template.md`
- Platform Profile: `references/platform-profile-template.md`
- Architecture Decision: `references/architecture-decision-template.md`
- Source Manifest: `references/source-manifest-template.md`
- Page-Source Map: `references/page-source-map-template.md`
- Repository / Process / System / Interface / Workflow / Platform Profile: `references/*-template.md`
- Init / Ingestion / Integration / Update / Lint / Review: `references/*-report-template.md`
- Human Review Summary: `references/human-review-summary-template.md`
- Human Decision: `references/human-decision-template.md`

v0.1.0 defines the Skill/Prompt workflow and its design contracts. It does not claim that a real business repository has passed an end-to-end POC.
