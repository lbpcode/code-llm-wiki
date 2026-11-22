# Page-Source Map Template

The Page-Source Map is the reverse index for incremental updates. Keep one entry per substantive Wiki page.

```yaml
schema_version: 1
pages:
  - page_id: <stable-page-id>
    path: wiki/processes/<process-id>/overview.md
    page_type: process
    content_status: draft # draft | approved | published | stale | superseded
    claim_ids:
      - <claim-id-1>
      - <claim-id-2>
    source_refs:
      - repository_id: <repository-id>
        commit: <full-40-character-commit-sha>
        paths:
          - src/main.cpp
        evidence_ids:
          - <evidence-id>
    depends_on_pages:
      - <page-id>
    last_reviewed_change_id: <change-id-or-null>
    last_reviewed_wiki_commit: <full-commit-sha-or-null>
    last_reviewed_at: <timestamp-or-null>
```

## Rules

- Update only after the page and referenced sources have been inspected.
- List paths at the granularity needed for impact analysis; avoid a generic repository-wide dependency unless the page truly depends on the entire repository.
- Include downstream page dependencies such as Process → Interface → Workflow → System.
- Keep source commits separate per repository.
- A missing or incomplete map makes impact analysis PARTIAL; do not assume no impact.
