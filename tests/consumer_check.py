#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


def run(*args: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout


def plan(*changed: str) -> list[str]:
    output = run("plan", "--repo", ".", "--changed", *changed, "--json")
    return [entry["id"] for entry in json.loads(output)]


def main() -> int:
    shutil.rmtree(ROOT / "build", ignore_errors=True)

    item_a = plan("qualification/item-a/input.txt")
    assert item_a == ["library-tests", "integration-example-a", "qualification-item-a"], item_a
    assert "qualification-item-b" not in item_a

    shared = plan("src/core.txt")
    assert shared == [
        "library-tests",
        "integration-example-a",
        "qualification-item-a",
        "qualification-item-b",
    ], shared

    first = run("run", "--repo", ".")
    assert "qualification-item-a:verify\tran" in first
    assert "qualification-item-b:verify\tran" in first

    second = run("run", "--repo", ".")
    assert "library-tests:test\treused" in second
    assert "integration-example-a:run-example\treused" in second
    assert "qualification-item-a:verify\treused" in second
    assert "qualification-item-b:verify\treused" in second

    exact = run("run", "--repo", ".", "--item", "qualification-item-a", "--step", "verify")
    lines = [line for line in exact.splitlines() if line.strip()]
    assert lines == ["qualification-item-a:verify\tran"], lines

    print("consumer checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
