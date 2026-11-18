#!/usr/bin/env python3
"""Prove that a main baseline can update one item without rebuilding siblings."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


def run(*args: str) -> str:
    """Run the pinned tool and return combined command output."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return completed.stdout


def tree_hash(root: Path) -> str:
    """Hash every file below one item directory in stable path order."""

    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def main() -> int:
    """Update only item-a in a complete baseline and preserve item-b."""

    out = ROOT / "output" / "main-update-check"
    shutil.rmtree(out, ignore_errors=True)
    baseline = out / "baseline"
    updated = out / "updated"

    run(
        "build",
        "prepare-main",
        "--repo",
        ".",
        "--candidate-root",
        "build",
        "--out",
        str(baseline),
        "--source-commit",
        "baseline",
    )

    sibling = baseline / "qualification" / "item-b"
    sibling_before = tree_hash(sibling)
    input_file = ROOT / "qualification" / "item-a" / "input.txt"
    original = input_file.read_text(encoding="utf-8")

    try:
        input_file.write_text("item-a-update-main\n", encoding="utf-8")
        run(
            "run",
            "--repo",
            ".",
            "--item",
            "qualification-item-a",
        )
        run(
            "build",
            "update-main",
            "--repo",
            ".",
            "--main",
            str(baseline),
            "--candidate-root",
            "build",
            "--out",
            str(updated),
            "--source-commit",
            "main-new",
            "--items",
            "qualification-item-a",
        )

        if tree_hash(updated / "qualification" / "item-b") != sibling_before:
            raise RuntimeError("unselected item-b changed during main update")

        old_a = tree_hash(baseline / "qualification" / "item-a")
        new_a = tree_hash(updated / "qualification" / "item-a")
        if old_a == new_a:
            raise RuntimeError("selected item-a was not replaced")
    finally:
        # Later consumer checks expect build/ to match the checked-out source.
        input_file.write_text(original, encoding="utf-8")
        run(
            "run",
            "--repo",
            ".",
            "--item",
            "qualification-item-a",
        )

    print("main update checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
