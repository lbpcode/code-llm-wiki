# Wiki Index Template

Render at `wiki/index.md` in Simplified Chinese by default. All links are relative to this file. The following is a shape to fill, not example project knowledge. Remove placeholder rows and empty entity groups; an empty Wiki explicitly states that no published knowledge exists.

```markdown
# <System name> Wiki

<Scope of this Wiki and how to identify published versus candidate knowledge.>

Maintenance instructions: [AGENTS.md](../AGENTS.md)
Operation history: [Log](log.md)

## Accepted and published knowledge

### <Entity category, e.g. Process>

| Page ID | Page | One-line summary | Process / Profiles | Content status | Owning change / publication state |
|---|---|---|---|---|---|
| <stable-page-id> | [<title>](<relative-page-path>) | <summary supported by this page> | <scope> | accepted | [<change-id>](<relative-change-record-path>) / published |

## Candidate, stale, and historical knowledge

| Entity type / Page ID | Page | One-line summary | Process / Profiles | Content status | Owning change / publication state |
|---|---|---|---|---|---|
| <type> / <stable-page-id> | [<title>](<relative-page-path>) | <bounded summary> | <scope> | <actual-status> | [<change-id>](<relative-change-record-path>) / <actual-change-status> |
```

Index every substantive page present in this snapshot once. Do not list each `_meta` record, ingestion report, or session handoff as a knowledge page. Retained historical pages remain labeled and linked; pending deletions must not make accepted pages vanish from accepted navigation. Derive visibility from page **and** Change Set state, not from a Claim's `verified` status. Follow docs/wiki-maintenance.md for publication transitions and missing-index fallback.
