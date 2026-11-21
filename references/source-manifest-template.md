# Source Manifest Template

The manifest is the provenance index for an ingestion run. Replace placeholders only with values discovered from the real superproject and repositories. Never invent repository names, commits, processes, or profile applicability.

    schema_version: 1
    system:
      id: <stable-system-id>
      name: <display-name>
    superproject:
      repository_id: <stable-repository-id>
      path: .
      commit: <full-commit-sha>
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
        commit: <full-commit-sha>
        branch: <informational-branch-name>
        agents_files:
          - AGENTS.md
        process_ids:
          - <process-id>
        platform_profile_ids:
          - qnx
          - android

## Rules

- Pin every repository to the exact commit checked out by the superproject/submodule.
- Record the superproject commit and each submodule commit independently.
- The remote URL is optional; never include credentials in it.
- A repository can implement multiple processes; a process can span multiple repositories.
- Only list profiles supported by evidence or explicitly confirmed project metadata.
- Unknown deployment context stays unknown.
- Keep secrets and environment-specific credentials out of the manifest.
- Update the manifest only after the corresponding source revision has been inspected.
