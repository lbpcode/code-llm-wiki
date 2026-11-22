# Source Manifest Template

The manifest is the provenance index for an ingestion run. Replace placeholders only with values discovered from the real superproject and repositories. Never invent repository names, commits, processes, or profile applicability.

```yaml
schema_version: 1
manifest_id: <stable-manifest-id>
generated_at: <ISO-8601-timestamp>
system:
  id: <stable-system-id>
  name: <display-name>
superproject:
  repository_id: <stable-repository-id>
  path: .
  commit: <full-40-character-commit-sha>
  branch: <informational-branch-name>
platform_profiles:
  - id: qnx
    os: QNX
    deployment_context: unknown
  - id: android
    os: Android
    deployment_context: unknown
  - id: linux-tbox
    os: Linux
    deployment_context: TBOX
repositories:
  - id: <repository-id>
    path: <submodule-path>
    remote: <canonical-repository-url-or-omitted>
    expected_commit: <full-40-character-superproject-pinned-sha>
    checked_out_commit: <full-40-character-actual-sha-or-null>
    checkout_status: matches_pin # matches_pin | mismatch | uninitialized | inaccessible
    branch: <informational-branch-name>
    agents_files:
      - path: AGENTS.md
        read_status: read # read | not_found | inaccessible | not_read
processes:
  - id: <process-id>
    display_name: <display-name>
    lifecycle_status: active # active | candidate | deprecated_candidate | retired_confirmed
repository_process_mappings:
  - repository_id: <repository-id>
    process_id: <process-id>
    status: confirmed # confirmed | candidate | unknown | rejected
    evidence_refs:
      - <evidence-id>
    responsibility_note: "<bounded responsibility>"
process_profile_mappings:
  - process_id: <process-id>
    profile_id: qnx
    support_status: supported_verified # supported_verified | present_unverified | unsupported_verified | unknown
    evidence_refs:
      - <evidence-id>
    constraints: []
```

## Rules

- Pin the superproject and every relevant repository to the exact full commit SHA inspected.
- For submodules, record both the expected pinned commit and actual checked-out commit. A mismatch blocks ingestion for that repository.
- For standalone source repositories, record the inspected commit as both expected_commit and checked_out_commit when applicable.
- Record AGENTS.md paths and whether each was read, absent, or inaccessible.
- Repository-to-Process and Process-to-Profile are separate mappings.
- A repository may implement multiple processes; a process may span multiple repositories.
- Process profile support must not be inferred from repository-level profile observations.
- Use `confirmed` only with direct evidence or explicit project-owner confirmation.
- Use `unknown` when evidence is insufficient; do not fill gaps with guesses.
- The remote URL is optional; never include credentials in it.
- Keep secrets and environment-specific credentials out of the manifest.
- Update the manifest only after the corresponding source revision has been inspected.
- Approval binds to the manifest version/digest and relevant source revisions. See docs/human-review.md.
