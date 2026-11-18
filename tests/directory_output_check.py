"""Prove recursive directory-output reuse against the pinned tool."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


def run(*args: str) -> list[str]:
    """Run the pinned tool and return non-empty output lines."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return [line for line in completed.stdout.splitlines() if line.strip()]


def main() -> int:
    """Tamper with a nested result and require only package to rerun."""

    nested = (
        ROOT
        / "build"
        / "qualification"
        / "item-a"
        / "results"
        / "nested"
        / "provenance.json"
    )
    if not nested.is_file():
        raise RuntimeError("consumer_check did not create the directory output")

    nested.write_text('{"status":"tampered"}\n', encoding="utf-8")
    lines = run(
        "run",
        "--repo",
        ".",
        "--item",
        "qualification-item-a",
    )

    expected = [
        "qualification-item-a:build\treused",
        "qualification-item-a:verify\treused",
        "qualification-item-a:package\tran",
    ]
    if lines != expected:
        raise RuntimeError(
            "unexpected directory-output rerun:\n"
            + "\n".join(lines)
        )

    restored = nested.read_text(encoding="utf-8")
    if "tampered" in restored:
        raise RuntimeError("package step did not restore nested directory output")

    print("directory output checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
