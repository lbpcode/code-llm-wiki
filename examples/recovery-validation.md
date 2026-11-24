# Synthetic recovery validation

This exercise checks the file/Git contracts in docs/snapshot-binding.md and docs/publication-recovery.md. It does not ingest a business repository or establish real human approval. The fixture generator creates inputs and checks final artifacts; it is not a recovery implementation or Wiki runtime.

## Reproduce

From the Skill repository, run:

```sh
python3 tests/recovery_fixture.py
```

The printed temporary directory contains two bare local Git repositories, a portable `handoff.json`, and two independent record registries. JSON is used as YAML-compatible encoding; retain that encoding when updating the fixture. Git and Python's standard library are sufficient to create/check the fixture.

Give a fresh Agent only the Skill package location, the generated handoff path, and this task:

> Read the Skill and applicable recovery contracts. Verify the two independent registry cases from handoff.json; do not substitute one registry for the other. For case A, resume the preauthorized local synthetic publication and then retry the same operation. For case B, report whether the frozen snapshot can proceed, without publishing. Inspect Query visibility before finalization, before completion, and after completion. Keep records of actual commits, event counts, integrity checks, and limitations. Mutate only the generated temporary fixture, preserving frozen bundles and source history. Do not access real remotes or claim that the synthetic gate/decision inputs are real approval.

The fixture deliberately starts after incorporation into the target but before its observed-commit checkpoint. It includes an added binary blob, a deleted file, an executable-bit change, and a human-authored page-body sentinel. Case B has altered patch bytes with unchanged expected hashes. Gate/decision records are minimal, explicitly synthetic inputs: this exercise tests recovery against their binding, not a complete Lint or independent semantic Review.

After the Agent finishes, run:

```sh
python3 tests/recovery_fixture.py --check /path/printed/by/setup
```

The checker verifies one finalization commit, one event artifact, page/change/index/receipt consistency, unchanged protected bytes/modes, preserved deletion, immutable bundle hashes, and unchanged source revision. Independently inspect the Agent's integrity and retry observations; the checker alone does not prove that an Agent rejected corruption or actually retried.

## Observed run (2026-11-24)

A fresh-context Agent followed the handoff and contracts without reading the artifact checker. The checker was then run separately and passed.

| Check | Observed result |
|---|---|
| Case A reconstruction | Resolved relative registry paths; reconstructed and verified the exact candidate tree, changed blobs/modes, manifest, and pinned source. |
| Case B altered patch | Digest mismatch blocked continuation; no replacement payload, approval reuse, or publication. Original case B records were preserved. |
| Interrupted publication | Reused the existing content commit; one metadata finalization commit changed the target's history count from 2 to 3 and event count from 0 to 1. |
| Same-publication retry | History count remained 3; event count remained 1; completed receipt bytes were unchanged. |
| Intermediate visibility | Withheld new knowledge after incorporation, after finalization but before receipt completion, and after event creation but before completion. |
| Preservation | Page body/human note, binary content, executable mode, deletion, source history, and frozen bundles were preserved; final page/change/index/receipt agreed. |

A separate read-only contract review found consistent candidate-only, Lint-without-Review, and full-workflow behavior across direct Ingest/Integrate/Update invocation. This was a textual consistency check, not execution of those three generation workflows. The exercise also prompted explicit wording for manifest schema version and attempt-report registration timing.

## Scope

The exercise covers a fresh context resolving relative handoff paths, patch-backed reconstruction, corruption blocking, publication interruption, and completed-operation retry. Real remote concurrency, crash injection at every checkpoint, credential expiry/revocation, and a real repository's full generation/review/publication workflow remain outside this exercise. Temporary storage is appropriate for this test only; production records require the durable registry and archive contract.
