# Destination Wiki AGENTS.md Template

Render this section in the destination Wiki repository's root `AGENTS.md`. Preserve text outside the managed section. Fill paths and package provenance from inspected inputs; render user-facing prose in Simplified Chinese by default. This is a template for the Wiki, not instructions to install into source repositories.

```markdown
<!-- CODE_LLM_WIKI_START -->
## Code LLM Wiki maintenance

### Entry points

- Wiki root: <repository-relative-wiki-root>
- Navigation: <wiki-root>/index.md
- Operation timeline: <wiki-root>/log.md
- Source inventory: <wiki-root>/_meta/source-manifest.yaml
- Source/page dependencies: <wiki-root>/_meta/page-source-map.yaml
- Change and review records: <wiki-root>/_meta/changes/
- Full workflow package: <repository-url-or-versioned-bundle-location>
- Package revision/digest: <verified-revision-or-snapshot-digest-and-dirty-provenance>
- Package entry: SKILL.md
- Query logging policy: `query_logging: disabled`

### Answering questions

Read the index of the selected accepted Wiki revision first, then relevant pages and their Claim/Evidence records. Use pages marked accepted only when the owning Change Set is published. Verify the underlying source revision and locator; identify stale, inferred, unknown, or conflicting information. Cite original repository, full commit, path, and line/symbol/configuration locator.

Query is read-only by default, including index and log. If navigation is incomplete, search relevant pages and disclose the gap without repairing files. An explicit read-only request overrides any logging policy. With query logging explicitly enabled, append only a redacted operation event; this grants no authority to edit knowledge, commit, or publish.

### Saving and maintaining knowledge

When the user requests retaining an answer, load the full workflow package and use Query → Update query-capture mode. Extend an existing appropriate page when possible. Link each new conclusion to original source evidence, preserve uncertainty, and prepare a draft Change Set with index, cross-link, and Page-Source Map updates.

For source changes, use Update with the previous manifest/map and the new pinned revisions. Read source only; preserve source code, submodule pins, human Wiki edits, and accepted history. On conflicting human changes, report the conflict rather than replacing their text.

Before a knowledge mutation, load the package's applicable schema, maintenance, state, evidence, and quality rules. If they cannot be located, explain the missing dependency; do not invent the workflow. These local instructions still support read-only navigation and answers.

### Checks and publication

Keep generated content candidate until Lint, a completed isolated host-native Review Subagent, human approval, and explicitly authorized publication. Review receives a fresh context without the generator transcript. Missing capability/checks are NOT RUN, not PASS. Preserve exact Wiki/source snapshot binding; never self-approve or silently push/merge.

Update navigation with candidate page changes. Log observed operations by append-only event ID. Lint/Review return events to the orchestrator; they do not edit their input. Write post-freeze events outside the reviewed snapshot and reconcile them later under existing authorization. Never change an approved diff merely to add a log entry.

Human-facing knowledge and reports default to Simplified Chinese. Preserve identifiers, paths, schema keys, status enums, and source excerpts verbatim.
<!-- CODE_LLM_WIKI_END -->
```
