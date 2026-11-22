# Claim and Evidence Record Template

Use one Claim per independently verifiable statement. Replace placeholders only with inspected values.

```yaml
claims:
  - claim_id: <stable-claim-id>
    statement: "<one atomic statement>"
    scope_type: process # system | repository | process | interface | workflow | profile
    scope_id: <stable-entity-id>
    profile_ids: [qnx] # [] only when genuinely platform-neutral
    status: unknown # verified | inferred | unknown | stale | contradicted
    evidence_refs:
      - evidence_id: <evidence-id>
        relation: supports # supports | contradicts | qualifies
    reasoning: null # required for inferred
    assumptions: []
    limitations: []
    last_verified_at: null

evidence:
  - evidence_id: <stable-evidence-id>
    repository_id: <manifest-repository-id>
    commit: <full-40-character-commit-sha>
    path: <repository-relative-path>
    locator_type: line_range # line_range | symbol | config_key | document_heading | artifact
    locator: "<exact locator>"
    evidence_type: implementation # implementation | declaration | configuration | build_graph | documentation | test | history
    profile_ids: [qnx]
    status: unverified # valid | unverified | stale | inaccessible | conflicting | redacted
    checked_at: null
    excerpt: null # optional; redact secrets and sensitive values
    redaction_reason: null
```

## Review questions

- Is the statement atomic and scoped?
- Does every material claim link to evidence?
- Does the evidence prove the exact statement and relationship type?
- Is the commit pinned and locator resolvable?
- Is platform scope justified?
- Are inference, assumptions, limitations, and unknowns explicit?
