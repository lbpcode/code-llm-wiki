# Snapshot Binding Record

Write immutable UTF-8/LF YAML at `bindings/<binding-id>/binding.yaml` in the external records registry. Payload paths below are relative to this file. Fill only inspected values. Hash the final bytes externally; do not add a self-digest to this record. Follow docs/snapshot-binding.md for storage, recovery, validation, and archival.

```yaml
schema_version: 1
binding_id: <unique-binding-id>
change_id: <change-id>
created_at: <ISO-8601-with-timezone>
wiki_repository_id: <stable-wiki-repository-id>
base_wiki_commit: <full-commit-sha>
candidate_wiki_commit: null # full commit when commit-backed; null when patch-backed
candidate_tree_oid: <exact-git-tree-oid>
patch:
  path: candidate.patch
  sha256: <sha256-of-exact-binary-patch-bytes>
source_manifest:
  path: wiki/_meta/source-manifest.yaml
  version: 1 # actual source manifest schema_version; digest identifies content
  sha256: <sha256-of-manifest-bytes-in-candidate>
source_revisions:
  - repository_id: <source-id>
    commit: <full-commit-sha>
changed_page_ids: []
changed_claim_ids: []
files:
  - path: <wiki-repository-relative-path>
    before: # null for an added path
      mode: "100644"
      sha256: <sha256-of-base-git-blob-bytes>
    after: # null for a deleted path
      mode: "100644"
      sha256: <sha256-of-candidate-git-blob-bytes>
publication_plan: null # or {path: publication-plan.yaml, sha256: <exact-bytes-digest>}
```

The common reference shape in Change Set, Review, Human Decision, and publication progress is:

```yaml
snapshot_binding_ref:
  registry_id: <authorized-registry-id>
  binding_id: <binding-id>
  record_path: bindings/<binding-id>/binding.yaml
snapshot_binding_sha256: <expected-record-digest> # external reports/decisions; null in frozen self-referencing content
```

Use the Git blob byte hash for all supported modes; absent sides are YAML null, not an empty file hash. List exactly the patch's changed paths. No-op or excluded paths cannot conceal candidate changes. Verification reports repeat the resolved candidate/source values and record whether each integrity/recovery check actually ran; missing checks cannot become PASS.
