# Language Policy

## 1. Default output language

Unless the user explicitly requests another language, all generated engineering knowledge and user-facing deliverables must use **Simplified Chinese**.

This applies to:
- Wiki pages at System, Process, Interface, and Workflow levels;
- architecture descriptions and platform comparisons;
- repository/process analysis and integration reports;
- update summaries and change-impact reports;
- independent LLM review reports and quality-gate findings;
- query answers derived from the Wiki.
- generated destination AGENTS.md prose, index summaries, operation logs, and query-capture records.

## 2. Skill and prompt language

The canonical Skill instructions and reusable prompt templates in this repository are written in **English**. Keep them concise, explicit, and portable across agent environments.

English Skill instructions do not imply that generated Wiki content should be English. Every workflow Skill must follow this language policy.

## 3. Preserve source identifiers verbatim

Never translate or rewrite identifiers needed to locate or understand the source. Preserve the original spelling and casing of:
- function, class, type, variable, namespace, and symbol names;
- API names, system calls, compiler flags, macros, and enum values;
- file paths, repository names, commit SHAs, branch names, and URLs;
- configuration keys, XML attributes, JSON/YAML keys, service names, and CMake targets;
- commands, log fragments, protocol fields, and source excerpts.

Keep source evidence exact. Do not translate code excerpts or alter line references.

## 4. Technical terminology

Use natural Simplified Chinese for explanations. Retain established English technical terms where they are clearer or are the terms engineers use in source code.

At first mention, introduce an English term with a concise Chinese explanation when helpful, for example:
- 进程间通信（IPC）
- 休眠与恢复（Suspend/Resume）
- 构建依赖（Build Dependency）
- 运行时依赖（Runtime Dependency）

Avoid awkward word-for-word translation and unnecessary Chinese/English duplication.

## 5. Machine-readable metadata

Keep schema keys, stable IDs, profile IDs, relationship types, status enums, and other machine-readable values in their canonical English form. Human-readable titles, descriptions, findings, and explanatory text should be Simplified Chinese by default.

Examples:
- `profile_id: linux-tbox`
- `status: verified`
- `relationship: runtime_depends_on`
- `title: TBOX 进程启动流程`

## 6. Diagrams and tables

Use Simplified Chinese for explanatory labels and descriptions. Preserve API names, process identifiers, service names, protocol fields, and other source identifiers verbatim.

## 7. Explicit user preference overrides

If the user explicitly requests English, bilingual output, or another language for a particular task or Wiki, follow that request for the specified scope. Do not silently change the default policy for unrelated content.
