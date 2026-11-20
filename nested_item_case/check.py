#!/usr/bin/env python3
"""Black-box nested item template and Git selection acceptance."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def git(repo: Path, *args: str) -> str:
    """Run Git in one synthetic consumer repository."""

    return subprocess.check_output(
        ["git", *args],
        cwd=repo,
        text=True,
    ).strip()


def main() -> int:
    """Prove nested template expansion and sibling isolation from outside."""

    source = fresh_case(SOURCE, "nested_item_case")
    subprocess.run(["git", "init", "--quiet"], cwd=source, check=True)
    subprocess.run(
        ["git", "config", "user.name", "tool.cad.ci.test"],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "tool.cad.ci.test@example.invalid"],
        cwd=source,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=source, check=True)
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "base"],
        cwd=source,
        check=True,
    )
    base = git(source, "rev-parse", "HEAD")

    build123d = source / "examples/attach-angle/build123d/model.py"
    build123d.write_text(
        build123d.read_text(encoding="utf-8") + "\n# changed\n",
        encoding="utf-8",
    )
    subprocess.run(
        ["git", "add", "examples/attach-angle/build123d/model.py"],
        cwd=source,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--quiet", "-m", "change build123d"],
        cwd=source,
        check=True,
    )
    head = git(source, "rev-parse", "HEAD")

    runner = source.parent / "nested_item_case_clone"
    shutil.rmtree(runner, ignore_errors=True)
    subprocess.run(
        ["git", "clone", "--quiet", str(source), str(runner)],
        check=True,
    )

    assert not (runner / "build").exists()
    assert not (runner / ".cache/cad-ci").exists()

    plan = json.loads(
        run_tool(
            "plan",
            "--repo",
            str(runner),
            "--base",
            base,
            "--head",
            head,
            "--json",
        )
    )
    assert plan == [
        {
            "id": "examples-attach-angle-build123d",
            "path": "examples/attach-angle/build123d",
            "kind": "reference",
            "reason": "affected",
        }
    ], plan

    run = run_tool(
        "run",
        "--repo",
        str(runner),
        "--base",
        base,
        "--head",
        head,
    )
    assert "built: examples-attach-angle-build123d:build" in run, run
    assert "examples-attach-angle-cadquery" not in run, run

    result = (
        runner
        / "build"
        / "examples"
        / "attach-angle"
        / "build123d"
        / "result.txt"
    )
    assert result.read_text(encoding="utf-8") == "build123d:shared\n"
    assert not (
        runner
        / "build"
        / "examples"
        / "attach-angle"
        / "cadquery"
    ).exists()

    print("nested_item_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
