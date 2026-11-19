#!/usr/bin/env python3
"""Black-box durable build and real generated-branch publication acceptance."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import read_json, run_tool

CASE = Path(__file__).resolve().parent


def git(*args: str) -> str:
    """Run Git in the actual test repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def source_event() -> tuple[str, str, str, int]:
    """Return event name, source SHA/ref and PR number."""

    event_name = os.environ["GITHUB_EVENT_NAME"]
    event = json.loads(
        Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")
    )
    if event_name == "pull_request":
        pull_request = event["pull_request"]
        return (
            event_name,
            pull_request["head"]["sha"],
            pull_request["head"]["ref"],
            int(event["number"]),
        )
    return (
        event_name,
        os.environ["GITHUB_SHA"],
        os.environ["GITHUB_REF_NAME"],
        0,
    )


def build_site(path: Path, source_sha: str, build_commit: str) -> None:
    """Write the minimal site required by the generic Pages publisher."""

    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)
    (path / "index.html").write_text(
        "<!doctype html><title>tool.cad.ci.test</title>"
        "<p>publication acceptance passed</p>\n",
        encoding="utf-8",
    )
    (path / "provenance.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "source_commit": source_sha,
                "build_commit": build_commit,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def assert_item_evidence(path: Path, expected_item: str) -> None:
    """Check the public evidence format in fetched durable output."""

    state = read_json(path)
    assert state["schema"] == 1
    assert state["engine"] == "scons"
    assert state["status"] == "pass"
    assert state["item"] == expected_item
    assert state["final_bundle_sha256"]


def local_build_store_checks(out: Path, source_sha: str) -> None:
    """Prove complete main, sparse overlay and resolved view locally."""

    local_main = out / "local-main"
    run_tool(
        "build",
        "prepare-main",
        "--repo",
        str(CASE),
        "--candidate-root",
        str(CASE / "build"),
        "--out",
        str(local_main),
        "--source-commit",
        source_sha,
    )
    assert (local_main / "items/a/.cad-ci/item.json").is_file()
    assert (local_main / "items/b/.cad-ci/item.json").is_file()

    overlay = out / "local-overlay"
    run_tool(
        "build",
        "prepare-pr",
        "--repo",
        str(CASE),
        "--candidate-root",
        str(CASE / "build"),
        "--out",
        str(overlay),
        "--source-commit",
        source_sha,
        "--pull-request",
        "999999",
        "--items",
        "publish-a",
    )
    assert (overlay / "items/a/.cad-ci/item.json").is_file()
    assert not (overlay / "items/b").exists()

    resolved = out / "local-resolved"
    run_tool(
        "build",
        "resolve",
        "--main",
        str(local_main),
        "--overlay",
        str(overlay),
        "--out",
        str(resolved),
    )
    assert (resolved / "items/a/result.txt").read_text() == "a\n"
    assert (resolved / "items/b/result.txt").read_text() == "b\n"


def main() -> int:
    event_name, source_sha, source_ref, pull_request = source_event()
    if git("rev-parse", "HEAD") != source_sha:
        raise RuntimeError("workflow checkout is not the event source commit")

    # Build the immutable case in place; generated output is ignored by Git.
    shutil.rmtree(CASE / "build", ignore_errors=True)
    shutil.rmtree(CASE / ".cache", ignore_errors=True)
    run_tool("run", "--repo", str(CASE))

    out = ROOT / "output" / "publish_case"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    local_build_store_checks(out, source_sha)

    # Source freshness is a safety boundary. A deliberately wrong expected
    # source SHA must be rejected before any generated branch is changed.
    stale_site = out / "stale-site"
    build_site(stale_site, source_sha, "not-published")
    stale = run_tool(
        "publish",
        "pages",
        "--repo",
        str(ROOT),
        "--site",
        str(stale_site),
        "--message",
        "This publication must be rejected",
        "--source-ref",
        source_ref,
        "--expected-source",
        "0" * 40,
        expect=2,
    )
    assert "moved" in stale or "expected" in stale

    if event_name == "pull_request":
        candidate = out / "pr"
        run_tool(
            "build",
            "prepare-pr",
            "--repo",
            str(CASE),
            "--candidate-root",
            str(CASE / "build"),
            "--out",
            str(candidate),
            "--source-commit",
            source_sha,
            "--pull-request",
            str(pull_request),
            "--items",
            "publish-a",
        )
        build_commit = run_tool(
            "publish",
            "build",
            "--repo",
            str(ROOT),
            "--candidate",
            str(candidate),
            "--scope",
            "pr",
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish tool.cad.ci.test PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ).strip()

        site = out / "site"
        build_site(site, source_sha, build_commit)
        run_tool(
            "publish",
            "pages",
            "--repo",
            str(ROOT),
            "--site",
            str(site),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish tool.cad.ci.test preview PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        generated = out / "generated-build"
        fetched = run_tool(
            "build",
            "fetch",
            "--repo",
            str(ROOT),
            "--out",
            str(generated),
        ).strip()
        assert fetched == build_commit
        evidence = (
            generated
            / f"pr/{pull_request}/items/a/.cad-ci/item.json"
        )
        assert_item_evidence(evidence, "publish-a")
        assert not (
            generated / f"pr/{pull_request}/items/b"
        ).exists()

        git("fetch", "--quiet", "origin", "gh-pages")
        preview = json.loads(
            git(
                "show",
                f"origin/gh-pages:previews/pr-{pull_request}/provenance.json",
            )
        )
        assert preview["source_commit"] == source_sha
        assert preview["build_commit"] == build_commit

        run_tool(
            "publish",
            "build-cleanup",
            "--repo",
            str(ROOT),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Clean tool.cad.ci.test PR #{pull_request} build",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )
        run_tool(
            "publish",
            "pages-cleanup",
            "--repo",
            str(ROOT),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Clean tool.cad.ci.test PR #{pull_request} preview",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        cleaned = out / "generated-build-cleaned"
        run_tool(
            "build",
            "fetch",
            "--repo",
            str(ROOT),
            "--out",
            str(cleaned),
        )
        assert not (cleaned / f"pr/{pull_request}").exists()

        git("fetch", "--quiet", "origin", "gh-pages")
        preview_check = subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"origin/gh-pages:previews/pr-{pull_request}/provenance.json",
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        assert preview_check.returncode != 0
    else:
        candidate = out / "main"
        run_tool(
            "build",
            "prepare-main",
            "--repo",
            str(CASE),
            "--candidate-root",
            str(CASE / "build"),
            "--out",
            str(candidate),
            "--source-commit",
            source_sha,
        )
        build_commit = run_tool(
            "publish",
            "build",
            "--repo",
            str(ROOT),
            "--candidate",
            str(candidate),
            "--scope",
            "main",
            "--message",
            f"Publish tool.cad.ci.test main {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        ).strip()

        site = out / "site"
        build_site(site, source_sha, build_commit)
        run_tool(
            "publish",
            "pages",
            "--repo",
            str(ROOT),
            "--site",
            str(site),
            "--message",
            f"Publish tool.cad.ci.test stable {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        generated = out / "generated-build"
        fetched = run_tool(
            "build",
            "fetch",
            "--repo",
            str(ROOT),
            "--out",
            str(generated),
        ).strip()
        assert fetched == build_commit
        assert_item_evidence(
            generated / "main/items/a/.cad-ci/item.json",
            "publish-a",
        )
        assert_item_evidence(
            generated / "main/items/b/.cad-ci/item.json",
            "publish-b",
        )

        git("fetch", "--quiet", "origin", "gh-pages")
        stable = json.loads(git("show", "origin/gh-pages:provenance.json"))
        assert stable["source_commit"] == source_sha
        assert stable["build_commit"] == build_commit

    print("publish_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
