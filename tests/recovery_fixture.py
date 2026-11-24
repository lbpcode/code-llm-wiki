#!/usr/bin/env python3
"""Synthetic fixtures for manual/Agent contract validation; not a Wiki runtime.

`python3 tests/recovery_fixture.py` creates isolated local Git repositories and
handoff records. It does not execute recovery, approval, or publication.
`python3 tests/recovery_fixture.py --check DIR` checks artifacts after an Agent
has followed the handoff. JSON is used as a YAML-compatible fixture encoding.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value if isinstance(value, bytes) else encoded(value))


def git(repo, *args, data=None, env=None):
    options = os.environ.copy()
    options.update({"GIT_AUTHOR_NAME": "Synthetic Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                    "GIT_COMMITTER_NAME": "Synthetic Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"})
    options.update(env or {})
    return subprocess.check_output(["git", "-C", str(repo), *args], input=data, env=options).strip()


def tree(repo, files):
    with tempfile.TemporaryDirectory() as temp:
        env = {"GIT_INDEX_FILE": str(Path(temp) / "index")}
        git(repo, "read-tree", "--empty", env=env)
        for path, (mode, data) in sorted(files.items()):
            blob = git(repo, "hash-object", "-w", "--stdin", data=data).decode()
            git(repo, "update-index", "--add", "--cacheinfo", mode, blob, path, env=env)
        return git(repo, "write-tree", env=env).decode()


def commit(repo, files, message, parent=None):
    oid = tree(repo, files)
    args = ["commit-tree", oid, "-m", message]
    if parent:
        args.extend(["-p", parent])
    return git(repo, *args).decode(), oid


def setup():
    root = Path(tempfile.mkdtemp(prefix="code-wiki-recovery-"))
    source, wiki = root / "source.git", root / "wiki.git"
    for repo in (source, wiki):
        subprocess.run(["git", "init", "--bare", "--quiet", str(repo)], check=True)
    source_commit, _ = commit(source, {"telemetry.py": ("100644", b'def wake():\n    return "ready"\n')}, "Synthetic source")
    git(source, "update-ref", "refs/heads/main", source_commit)
    registry = root / "records"
    ref = {"registry_id": "synthetic-records", "binding_id": "binding-001", "record_path": "bindings/binding-001/binding.yaml"}
    pubref = {"registry_id": "synthetic-records", "publication_id": "publish-001", "record_path": "publications/publish-001/progress.yaml"}
    page = "wiki/processes/telemetry/overview.md"
    manifest_path = "wiki/_meta/source-manifest.yaml"
    change_path = "wiki/_meta/changes/change-001/change-set.yaml"
    manifest = {"schema_version": 1, "manifest_id": "synthetic", "source_revisions": [{"repository_id": "source", "commit": source_commit}]}
    page_body = b'# Telemetry\n\nThe wake function returns "ready".\n\n<!-- HUMAN_NOTE_PRESERVE -->\n'
    page_bytes = b"---\nid: process.telemetry.overview\ncontent_status: candidate\nchange_id: change-001\n---\n" + page_body
    index = b"# Synthetic Wiki\n\n## Accepted and published\n\n## Candidate\n\n| page_id | page | summary | content_status | change_status |\n|---|---|---|---|---|\n| process.telemetry.overview | [Telemetry](processes/telemetry/overview.md) | Wake return value | candidate | draft |\n"
    base_files = {manifest_path: ("100644", encoded(manifest)), "obsolete.md": ("100644", b"Synthetic obsolete page\n"), "helper.sh": ("100644", b"#!/bin/sh\nexit 0\n")}
    base, _ = commit(wiki, base_files, "Synthetic Wiki baseline")
    change = {"change_id": "change-001", "status": "draft", "snapshot_binding_ref": ref,
              "snapshot_binding_sha256": None, "publication_record_ref": pubref,
              "publication": {"authorized": False, "published_commit": None}}
    candidate_files = {manifest_path: base_files[manifest_path], "helper.sh": ("100755", base_files["helper.sh"][1]),
                       page: ("100644", page_bytes), "wiki/index.md": ("100644", index),
                       "wiki/assets/payload.bin": ("100644", bytes(range(256))), change_path: ("100644", encoded(change))}
    content_commit, candidate_tree = commit(wiki, candidate_files, "Synthetic frozen candidate", base)
    # Exact patch bytes must retain their final newline; the general git helper strips output.
    patch = subprocess.check_output(["git", "-C", str(wiki), "diff", "--binary", "--no-ext-diff", "--no-renames", base, content_commit])
    transitions = [{"path": page, "selector": "frontmatter.content_status", "before": "candidate", "after": "accepted"},
                   {"path": change_path, "selector": "status", "before": "draft", "after": "published"},
                   {"path": change_path, "selector": "publication.authorized", "before": False, "after": True},
                   {"path": change_path, "selector": "publication.published_commit", "before": None, "after_from": "observed_content_commit"}]
    plan = {"schema_version": 1, "plan_id": "plan-001", "change_id": "change-001",
            "target": {"repository_id": "wiki", "branch": "published", "expected_commit": base},
            "transitions": transitions, "index_transitions": [{"path": "wiki/index.md", "page_id": "process.telemetry.overview",
                "before_content_status": "candidate", "after_content_status": "accepted", "before_change_status": "draft",
                "after_change_status": "published", "move_to": "accepted-and-published"}], "artifacts": []}
    bundle = registry / "bindings/binding-001"
    write(bundle / "candidate.patch", patch)
    write(bundle / "publication-plan.yaml", plan)
    def entry(value):
        return None if value is None else {"mode": value[0], "sha256": sha(value[1])}
    files = [{"path": p, "before": entry(base_files.get(p)), "after": entry(candidate_files.get(p))}
             for p in sorted(set(base_files) | set(candidate_files)) if base_files.get(p) != candidate_files.get(p)]
    binding = {"schema_version": 1, "binding_id": "binding-001", "change_id": "change-001", "created_at": "2026-11-24T16:00:00+08:00",
               "wiki_repository_id": "wiki", "base_wiki_commit": base, "candidate_wiki_commit": None, "candidate_tree_oid": candidate_tree,
               "patch": {"path": "candidate.patch", "sha256": sha(patch)},
               "source_manifest": {"path": manifest_path, "version": 1, "sha256": sha(encoded(manifest))},
               "source_revisions": manifest["source_revisions"], "changed_page_ids": ["process.telemetry.overview"], "changed_claim_ids": [],
               "files": files, "publication_plan": {"path": "publication-plan.yaml", "sha256": sha(encoded(plan))}}
    write(registry / "registry.yaml", {"schema_version": 1, "registry_id": "synthetic-records", "wiki_repository_id": "wiki"})
    write(bundle / "binding.yaml", binding)
    binding_digest = sha(encoded(binding))
    # All gate/decision/authorization records below are explicitly synthetic inputs.
    common = {"change_id": "change-001", "snapshot_binding_ref": ref, "snapshot_binding_sha256": binding_digest, "synthetic_fixture": True}
    for kind in ("lint", "review"):
        write(registry / f"changes/change-001/{kind}.yaml", {**common, "report_id": kind + "-001", "result": "PASS"})
    decision = {**common, "human_decision_id": "decision-001", "decision": "approve", "reviewer": "synthetic fixture",
                "base_wiki_commit": base, "candidate_wiki_commit": None, "diff_digest": sha(patch),
                "source_manifest_digest": sha(encoded(manifest)), "source_revisions": manifest["source_revisions"],
                "lint_report_id": "lint-001", "review_report_id": "review-001", "publication_plan_sha256": sha(encoded(plan))}
    decision_path = "changes/change-001/human-decision.yaml"
    write(registry / decision_path, decision)
    authorization = {**common, "schema_version": 1, "authorization_id": "authorization-001", "human_authorizer": "synthetic fixture",
                     "human_decision_ref": decision_path, "human_decision_sha256": sha(encoded(decision)),
                     "plan_sha256": sha(encoded(plan)), "target": plan["target"], "resolved_artifacts": [], "constraints": ["local synthetic repositories only"]}
    auth_path = "publications/publish-001/authorization.yaml"
    write(registry / auth_path, authorization)
    progress = {"schema_version": 1, "publication_id": "publish-001", **common, "plan_ref": "publication-plan.yaml", "plan_sha256": sha(encoded(plan)),
                "human_decision_ref": decision_path, "human_decision_sha256": sha(encoded(decision)),
                "publication_authorization_ref": auth_path, "publication_authorization_sha256": sha(encoded(authorization)),
                "target": {"repository_id": "wiki", "branch": "published", "expected_start_commit": base},
                "prepared_content_commit": content_commit, "observed_content_commit": None,
                "prepared_finalization_commit": None, "observed_finalization_commit": None, "last_verified_target_commit": None,
                "event_id": "publish-001.publish", "event_ref": "publications/publish-001/publish-event.yaml", "event_written": False,
                "completed": False, "attempt_report_refs": [], "updated_at": "2026-11-24T16:00:00+08:00"}
    write(registry / pubref["record_path"], progress)
    # Interrupt after incorporation, before its observed-commit checkpoint.
    git(wiki, "update-ref", "refs/heads/published", content_commit)
    # A separate test case has the same handoff values but altered payload bytes.
    shutil.copytree(registry, root / "records-case-b")
    with (root / "records-case-b/bindings/binding-001/candidate.patch").open("ab") as f:
        f.write(b"\n# altered after handoff\n")
    baseline = {"root": str(root), "base": base, "source_commit": source_commit, "content_commit": content_commit,
                "candidate_tree": candidate_tree, "binding_digest": binding_digest, "page": page, "change_path": change_path,
                "protected": {p: {"mode": mode, "sha256": sha(data)} for p, (mode, data) in candidate_files.items() if p not in (page, change_path, "wiki/index.md")},
                "page_body_sha256": sha(page_body), "immutable_hashes": {str(p.relative_to(registry)): sha(p.read_bytes()) for p in bundle.iterdir()}}
    write(root / "baseline.json", baseline)
    handoff = {"synthetic_only": True, "wiki_repository": "wiki.git", "source_repositories": {"source": "source.git"},
               "case_a_registry": "records", "case_b_registry": "records-case-b", "snapshot_binding_ref": ref,
               "snapshot_binding_sha256": binding_digest, "publication_record_ref": pubref,
               "requested_scope": "Verify each independent binding case. Resume local case A publication from durable records and then retry the completed operation. No external services or real approvals."}
    write(root / "handoff.json", handoff)
    print(root)


def check(root):
    baseline = json.loads((root / "baseline.json").read_text())
    registry, wiki = root / "records", root / "wiki.git"
    progress = json.loads((registry / "publications/publish-001/progress.yaml").read_text())
    final = git(wiki, "rev-parse", "refs/heads/published").decode()
    assert progress["completed"] is True and progress["observed_finalization_commit"] == final
    assert progress["observed_content_commit"] == baseline["content_commit"]
    assert git(wiki, "rev-list", "--count", baseline["content_commit"] + ".." + final) == b"1", "Repeated incorporation/finalization"
    assert git(wiki, "ls-tree", final, "obsolete.md") == b"", "Deleted candidate file reappeared"
    for path, expected in baseline["protected"].items():
        blob = subprocess.check_output(["git", "-C", str(wiki), "show", final + ":" + path])
        assert sha(blob) == expected["sha256"], path
        assert git(wiki, "ls-tree", final, path).decode().split()[0] == expected["mode"], path
    page = subprocess.check_output(["git", "-C", str(wiki), "show", final + ":" + baseline["page"]])
    assert b"content_status: accepted" in page
    assert sha(page.split(b"---\n", 2)[2]) == baseline["page_body_sha256"]
    change = json.loads(git(wiki, "show", final + ":" + baseline["change_path"]))
    assert change["status"] == "published" and change["publication"]["authorized"] is True
    assert change["publication"]["published_commit"] == baseline["content_commit"]
    index = git(wiki, "show", final + ":wiki/index.md")
    assert index.count(b"Wake return value") == 1 and b"| accepted | published |" in index
    assert index.index(b"## Accepted and published") < index.index(b"Wake return value") < index.index(b"## Candidate")
    events = list((registry / "publications/publish-001").glob("publish-event.yaml"))
    assert len(events) == 1 and progress["event_written"] is True
    for path, expected in baseline["immutable_hashes"].items():
        assert sha((registry / path).read_bytes()) == expected, path
    assert git(root / "source.git", "rev-parse", "refs/heads/main").decode() == baseline["source_commit"]
    print("PASS: one finalization commit, one event artifact, protected bytes/modes and frozen binding preserved, page/change/index/receipt consistent")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    check(args.check.resolve()) if args.check else setup()
