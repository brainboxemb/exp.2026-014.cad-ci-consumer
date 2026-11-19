#!/usr/bin/env python3
"""End-to-end checks for the synthetic tool.cad.ci consumer."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


def run(*args: str) -> str:
    """Run cad-ci successfully and return combined output."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout


def run_fail(*args: str) -> str:
    """Run cad-ci expecting failure and return its diagnostic output."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert completed.returncode != 0, completed.stdout
    return completed.stdout


def plan(*changed: str) -> list[str]:
    """Return ordered item IDs selected for synthetic changed paths."""

    output = run("plan", "--repo", ".", "--changed", *changed, "--json")
    return [entry["id"] for entry in json.loads(output)]


def main() -> int:
    """Prove selection, reuse, partial reruns and fan-in aggregation."""

    shutil.rmtree(ROOT / "build", ignore_errors=True)

    # A direct-only fan-in summary must not widen an ordinary item change.
    item_a = plan("qualification/item-a/input.txt")
    assert item_a == [
        "library-tests",
        "integration-example-a",
        "qualification-item-a",
    ], item_a
    assert "qualification-item-b" not in item_a
    assert "final-summary" not in item_a

    # Shared inputs still reach all normal dependants, but not the direct-only
    # summary unless the summary itself is selected.
    shared = plan("src/core.txt")
    assert shared == [
        "library-tests",
        "integration-example-a",
        "qualification-item-a",
        "qualification-item-b",
    ], shared
    assert "final-summary" not in shared

    # Changing the summary itself expands both dependency branches in order.
    summary = plan("qualification/summary/run.py")
    assert summary == [
        "library-tests",
        "integration-example-a",
        "qualification-item-a",
        "qualification-item-b",
        "final-summary",
    ], summary

    # A full run includes every item and produces the final summary.
    first = run("run", "--repo", ".")
    assert "qualification-item-a:verify\tran" in first
    assert "qualification-item-b:verify\tran" in first
    assert "final-summary:summarize\tran" in first
    assert (
        ROOT / "build/qualification/summary/summary.txt"
    ).read_text(encoding="utf-8") == "item-a:ok\nitem-b:ok\n"

    # A second unchanged run reuses the complete fan-in graph.
    second = run("run", "--repo", ".")
    assert "library-tests:test\treused" in second
    assert "integration-example-a:run-example\treused" in second
    assert "qualification-item-a:verify\treused" in second
    assert "qualification-item-b:verify\treused" in second
    assert "final-summary:summarize\treused" in second

    # Exact step reruns remain local to the named item.
    exact = run(
        "run",
        "--repo",
        ".",
        "--item",
        "qualification-item-a",
        "--step",
        "verify",
    )
    lines = [line for line in exact.splitlines() if line.strip()]
    assert lines == ["qualification-item-a:verify\tran"], lines

    # A partial dependency is not considered complete by a partial summary run.
    shutil.rmtree(ROOT / "build", ignore_errors=True)
    partial = run(
        "run",
        "--repo",
        ".",
        "--item",
        "qualification-item-a",
        "--until",
        "verify",
    )
    assert "qualification-item-a:verify\tran" in partial
    assert not (
        ROOT / "build/qualification/item-a/item.json"
    ).exists()

    failed = run_fail(
        "run",
        "--repo",
        ".",
        "--item",
        "final-summary",
        "--step",
        "summarize",
    )
    assert "requires a current result for qualification-item-a" in failed

    # Running the summary normally from a partial/clean graph completes every
    # dependency first and then writes the aggregate result.
    complete = run("run", "--repo", ".", "--item", "final-summary")
    assert "qualification-item-a:package\tran" in complete
    assert "qualification-item-b:verify\tran" in complete
    assert "final-summary:summarize\tran" in complete

    print("consumer checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
