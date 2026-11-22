# Code LLM Wiki

一套以 **Skill / Prompt** 驱动的代码知识沉淀工作流，面向由多个独立进程/服务仓库组成的工程系统。

核心目标：从 Superproject、Git Submodules、源码和现有工程文档中提取有证据支撑的知识，以 Process 为基本单元组织，再整合成 System 级架构知识，最终沉淀到独立 Wiki 仓库。

## v0.1.0 设计范围

- **知识模型**：Process 为核心，System 为跨进程知识整合层。
- **仓库关系**：Repository 与 Process 为多对多关系。
- **平台范围**：QNX、Android、Linux（TBOX）。
- **平台建模**：通过 Platform Profile 区分平台共性和特有实现。
- **源码证据**：重要结论关联仓库、commit 和源码位置。
- **构建关系**：可选使用 CMake Graphviz DOT 辅助分析 Target 级依赖。
- **AST**：第一阶段暂不引入。
- **质量门禁**：源码证据、独立 LLM 复核、人工批准。
- **输出语言**：Skill 指令以英文维护；Wiki 和报告默认简体中文。

## 工作流

```text
Init
  -> Ingest (per Repository / Process)
  -> Integrate (System-level)
  -> Lint
  -> Independent Review
  -> Human Approval
  -> Wiki Update
```

- `init`：盘点 Superproject、Submodules、AGENTS.md、commit 和平台信息。
- `ingest`：分析单个 Repository / Process，生成带源码证据的知识页面。
- `integrate`：整合多个 Process，形成 System 级架构知识。
- `query`：基于 Wiki 和源码证据回答工程问题。
- `update`：根据源码变化生成候选知识更新。
- `review`：独立复核知识结论、证据和关系。
- `lint`：检查结构、链接、证据、平台范围和一致性。

## 仓库结构

- `SKILL.md`：入口 Skill 与工作流路由。
- `skills/`：7 个独立工作流 Skill。
- `docs/`：架构、知识 Schema、证据规范、质量门禁、语言规范和设计决策。
- `references/`：平台定义、知识模板、清单和审核规范。
- `examples/`：示例材料。

## 核心约束

- 不按目录结构机械划分 Process。
- 区分 Build Dependency、Runtime Dependency、IPC 和 Startup Ordering。
- CMake DOT 只能作为构建关系证据，不能据此推断运行时关系。
- 平台共性必须有证据支撑；未知内容标记为 Unknown。
- 生成内容在通过独立复核和人工批准前，只是候选知识。
- Wiki 与源码分开存储，并记录对应的源码版本。
- 增量更新不得覆盖未经确认的人工修订。

详见 `docs/architecture.md`、`docs/wiki-schema.md`、`docs/source-evidence.md`、`docs/quality-gate.md` 和 `docs/language-policy.md`。
