# Wiki Navigation and Maintenance

## 1. Purpose and scope

This contract completes the persistent Wiki maintenance loop: discover knowledge through an index, record operations, retain useful query results, and let another Agent resume maintenance from the Wiki repository itself.

It adapts [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) to source-grounded engineering knowledge. That document describes a configurable pattern, not a fixed directory standard or certification. Source repositories at pinned commits serve as the raw-source layer; copying them into a `raw/` directory is unnecessary.

## 2. Wiki-local entry point

Init creates `AGENTS.md` at the **destination Wiki repository root** using references/wiki-agents-template.md. Preserve existing instructions: add or update a clearly delimited Code LLM Wiki section, propose the diff, and report conflicting instructions rather than replacing the file. Do not edit source-repository instructions.

The rendered entry point must contain:
- the actual Wiki root, index, log, manifest, map, and change-record paths;
- the read-only Query procedure, accepted/published trust policy, and citation rules;
- the candidate write, human-edit preservation, and quality/publication boundaries;
- the query capture and logging policy;
- a reproducible locator for the full Skill package: repository URL plus exact inspected revision and entry path, or a versioned bundled copy. A machine-specific installation path may be an additional convenience, never the only locator.

Fill these values from inspected inputs. Do not fabricate a package revision. If the package is modified locally, record its base commit and dirty status and use a preserved full package snapshot/digest or an explicitly identified pending locator; do not claim the base commit contains uncommitted changes. Reading published knowledge can use the self-contained local instructions; a workflow whose full rules are unavailable must report that limitation before mutating knowledge.

The local entry point is an instruction file, not a factual engineering page. Generated prose defaults to Simplified Chinese; preserve keys, paths, IDs, and status values.

## 3. Content index and page links

Maintain `wiki/index.md` using references/wiki-index-template.md. Each substantive page present in the selected Wiki snapshot has one canonical entry with its stable page ID, relative Markdown link, one-line summary, entity type, Process/Profile scope, page content status, owning Change ID, and publication state resolved from that Change Set.

- Group entries by System, Process, Repository, Interface, Workflow, Platform Profile, and Architecture Decision. Separate current accepted/published entries from candidate, stale, and historical entries. State explicitly when there is no published knowledge yet.
- Derive summaries from the linked pages; do not introduce new engineering claims in the index. If a page and its Change Set disagree, flag the inconsistency instead of assigning a more trusted status.
- Synchronize entries whenever Init, Ingest, Integrate, Update, or query capture adds, changes, moves, or supersedes pages. Put index edits in the same candidate diff as the page edits. Update publication visibility with the authorized publication state transition, and include the intended metadata transition in the review package.
- Query reads the index of the selected accepted snapshot first, then verifies page/change status and evidence. An index entry is navigation, not proof or an approval. If the index is missing/incomplete, fall back to scoped page discovery, disclose the limitation, and do not repair it during a read-only query.
- Add contextual relative Markdown links between related knowledge pages. Repository/Process pages should link to relevant interfaces, workflows, and system views. A bare ID in YAML is not a navigable page link. Standard Markdown links are sufficient; Obsidian-specific syntax is optional.

The index must reach every substantive page. Lint also reports pages with no meaningful inbound link outside the index, missing cross-references, and important concepts that may merit a page. These are maintenance findings, not a requirement to invent content or create empty pages; an intentionally standalone page can have a recorded rationale.

## 4. Operation log

Maintain `wiki/log.md` with references/wiki-log-template.md. It is an append-only operation timeline, distinct from the detailed reports under `_meta/changes/`. Use a stable event ID, timestamp with timezone, operation, scope, actual outcome, relevant Wiki/source revisions, and links to pages/reports. Operations include `init`, `ingest`, `integrate`, `query`, `capture`, `update`, `lint`, `review`, and `publish`.

- Log completion, partial work, or failure after the outcome is observed. Never pre-record PASS, approval, or publication. A correction is a new event referencing the old event ID; retries use new event IDs, while retrying the same append must not duplicate an existing ID.
- Logs summarize activity and link to findings; they are not engineering evidence or an alternative publication registry. Do not copy full conversations or sensitive inputs into them.
- For workflows already authorized to write the candidate Wiki, the orchestrator appends the event in that writable scope. Lint and Review remain read-only; they return their event to the orchestrator rather than editing the candidate.
- Ordinary Query remains read-only, including the log. Query logging is opt-in through an explicit request or an existing Wiki-local policy authorizing log-only writes. The default generated policy is `query_logging: disabled`. When disabled, return a compact event in the answer only when requested; do not write a file or ask for permission on every query. An enabled policy authorizes only log append, not page/index/claim changes, commits, or publication. A strictly read-only request overrides logging policy.
- Freeze the candidate snapshot before checks/review. Events and reports produced after freezing go to an authorized execution/report workspace outside that snapshot, or are returned to the caller if none exists. Reconcile pending events into the log as a subsequent audit change under existing authorization. Do not amend the frozen candidate, silently exclude log edits from its digest, or claim pending events were persisted. Publication must still match the approved candidate; any knowledge or index-summary change requires normal revalidation.
- Snapshot binding, live state records, and narrowly scoped publication metadata finalization follow docs/human-review.md sections 4 and 7. Canonical report paths describe archival placement, not permission to edit a frozen tree. An explicitly requested candidate-only run may stop before later gates, with their non-execution reported honestly.
- Use docs/snapshot-binding.md for portable records and fresh-session checks, and docs/publication-recovery.md for interruption recovery and once-only publication events. A retry of the same publication reuses its event ID; it is not a new publish operation.
- Serialize appends through one orchestrator. On concurrent changes, reread and merge events by ID without replacing or reordering existing history; report unresolved conflicts.

This policy intentionally allows an unlogged read-only query. It does not promise a complete query history when logging is disabled.

## 5. Query-to-knowledge capture

Query answers first. If the user requests saving, documenting, or updating the Wiki, route that authorized scope to the query-capture mode of `code-wiki-update`. Existing authorization persists; do not ask for the same permission again. Otherwise keep the answer read-only and, when useful, identify a concrete page that could be improved without creating a draft file.

Capture proceeds as follows:
1. Verify the accepted Wiki base, current source revisions, destination, and human edits. Use references/query-capture-template.md to record the question, bounded findings, source/Claim references, and intended page changes under a **new draft Change Set**.
2. Search the index and existing pages. Extend the appropriate Process, Interface, Workflow, or System page before creating a duplicate Q&A page. A question spanning processes may belong in a System or Workflow page; keep existing schema types.
3. Distinguish reused facts from new conclusions. Existing claims retain their IDs and evidence; a newly derived conclusion gets its own Claim and original source evidence with inference/assumptions where applicable. A chat answer or Wiki summary is not primary evidence.
4. Inspect missing evidence through bounded Ingest tasks if that read scope is authorized. Otherwise record the gap and leave the claim unknown. Never turn a plausible answer into a verified claim merely because the user wants to save it.
5. Prepare candidate page, Claim/Evidence, Page-Source Map, cross-link, and index changes. Preserve accepted pages and human text. Record the capture event and update report.
6. Run the same Lint → isolated Review → Human Review → authorized Publication sequence as a source-driven Update. Source commits may be unchanged; the knowledge diff still requires review. A no-op capture is reported as such, without inventing a new claim or publishing an empty change.

## 6. Administrative files and validation

`AGENTS.md`, `wiki/index.md`, and `wiki/log.md` are administrative files, not substantive knowledge pages. They do not need artificial Claim/Evidence records or Page-Source Map entries. Their links, status summaries, preserved history, and instructions are still checked. Substantive claims belong in evidence-backed pages, not in these files.

Use the same snapshot for index/page/state comparisons. Lint validates the local entry point, index coverage and links, log append-only behavior against the base revision, and capture provenance where applicable. Review checks semantic accuracy of index summaries and captured conclusions. No maintenance artifact grants approval or changes the canonical state enums.

For an existing Wiki, propose missing entry/index/log files in a bounded maintenance change; preserve existing pages, IDs, human instructions, and history. Do not backfill fictitious operation events. Historical events may be imported only from actual records, with their origin and original event time distinguished from the import time. A missing maintenance artifact may permit a disclosed read-only query, but required maintenance checks must pass before publishing a new knowledge change.
