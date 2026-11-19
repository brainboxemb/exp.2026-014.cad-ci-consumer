#!/usr/bin/env python3
"""Exercise the v0.2 build-store and Pages flow against the real GitHub repo."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


def run(*args: str) -> str:
    """Run the pinned cad-ci checkout and return its combined output."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    """Run Git in the consumer checkout for post-publication verification."""

    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
    ).strip()


def source_event() -> tuple[str, str, str, str, int]:
    """Return event name, base/source SHAs, source ref and PR number."""

    event_name = os.environ["GITHUB_EVENT_NAME"]
    event_path = Path(os.environ["GITHUB_EVENT_PATH"])
    event = json.loads(event_path.read_text(encoding="utf-8"))

    if event_name == "pull_request":
        pull_request = event["pull_request"]
        return (
            event_name,
            pull_request["base"]["sha"],
            pull_request["head"]["sha"],
            pull_request["head"]["ref"],
            int(event["number"]),
        )
    return (
        event_name,
        "",
        os.environ["GITHUB_SHA"],
        os.environ["GITHUB_REF_NAME"],
        0,
    )


def main() -> int:
    """Publish PR or main output and verify the exact generated branch paths."""

    event_name, base_sha, source_sha, source_ref, pull_request = source_event()

    # The candidate must be built from the same commit that freshness checks
    # protect. The workflow checks out the PR head explicitly for this reason.
    actual_checkout = git("rev-parse", "HEAD")
    if actual_checkout != source_sha:
        raise RuntimeError(
            f"checkout/source mismatch: expected {source_sha}, found {actual_checkout}"
        )

    out = ROOT / "output"
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)

    if event_name == "pull_request":
        overlay = out / "pr"
        run(
            "build",
            "prepare-pr",
            "--repo",
            ".",
            "--candidate-root",
            "build",
            "--out",
            str(overlay),
            "--source-commit",
            source_sha,
            "--pull-request",
            str(pull_request),
            "--base",
            base_sha,
            "--head",
            source_sha,
        )
        build_commit = run(
            "publish",
            "build",
            "--repo",
            ".",
            "--candidate",
            str(overlay),
            "--scope",
            "pr",
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish synthetic PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        site = out / "site"
        subprocess.run(
            [
                sys.executable,
                "site/build.py",
                "--out",
                str(site),
                "--source-commit",
                source_sha,
                "--build-commit",
                build_commit,
                "--base-path",
                f"/exp.2026-014.cad-ci-consumer/previews/pr-{pull_request}",
            ],
            cwd=ROOT,
            check=True,
        )
        run(
            "publish",
            "pages",
            "--repo",
            ".",
            "--site",
            str(site),
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish synthetic preview PR #{pull_request}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        git("fetch", "--quiet", "origin", "build", "gh-pages")
        state = git(
            "show",
            f"origin/build:pr/{pull_request}/qualification/item-a/item.json",
        )
        if json.loads(state).get("status") != "pass":
            raise RuntimeError("published PR build item is not passing")
        provenance = json.loads(
            git(
                "show",
                f"origin/gh-pages:previews/pr-{pull_request}/provenance.json",
            )
        )
        if provenance.get("source_commit") != source_sha:
            raise RuntimeError("preview provenance does not match PR source")
    else:
        main_candidate = out / "main"
        run(
            "build",
            "prepare-main",
            "--repo",
            ".",
            "--candidate-root",
            "build",
            "--out",
            str(main_candidate),
            "--source-commit",
            source_sha,
        )
        build_commit = run(
            "publish",
            "build",
            "--repo",
            ".",
            "--candidate",
            str(main_candidate),
            "--scope",
            "main",
            "--message",
            f"Publish synthetic main at {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        site = out / "site"
        subprocess.run(
            [
                sys.executable,
                "site/build.py",
                "--out",
                str(site),
                "--source-commit",
                source_sha,
                "--build-commit",
                build_commit,
                "--base-path",
                "/exp.2026-014.cad-ci-consumer",
            ],
            cwd=ROOT,
            check=True,
        )
        run(
            "publish",
            "pages",
            "--repo",
            ".",
            "--site",
            str(site),
            "--message",
            f"Publish synthetic stable site at {source_sha}",
            "--source-ref",
            source_ref,
            "--expected-source",
            source_sha,
        )

        git("fetch", "--quiet", "origin", "build", "gh-pages")
        state = git(
            "show",
            "origin/build:main/qualification/item-b/item.json",
        )
        if json.loads(state).get("status") != "pass":
            raise RuntimeError("published main build is incomplete")
        provenance = json.loads(
            git("show", "origin/gh-pages:provenance.json")
        )
        if provenance.get("source_commit") != source_sha:
            raise RuntimeError("stable provenance does not match main source")

    print("publication checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
