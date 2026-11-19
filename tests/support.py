"""Shared process helpers for independent released-stack acceptance cases.

This module only invokes the exact pinned tool checkout and creates disposable
case copies. Acceptance semantics stay in each case's own check.py.
"""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"
WORK_ROOT = ROOT / "output" / "cases"


def fresh_case(source: Path, name: str) -> Path:
    """Copy one immutable case template to disposable output/cases/<name>."""

    target = WORK_ROOT / name
    shutil.rmtree(target, ignore_errors=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns(
            "check.py",
            "__pycache__",
            "build",
            ".cache",
        ),
    )
    return target


def run_tool(
    *args: str,
    cwd: Path | None = None,
    expect: int = 0,
) -> str:
    """Run the exact bootstrapped tool and return combined output."""

    completed = subprocess.run(
        [sys.executable, str(CAD_CI), *args],
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != expect:
        raise AssertionError(
            f"cad-ci exit {completed.returncode}, expected {expect}\n"
            f"command: {' '.join(args)}\n"
            f"{completed.stdout}"
        )
    return completed.stdout


def remove_local_scons_state(repo: Path, *, keep_cache: bool) -> None:
    """Simulate a fresh runner, optionally preserving only SCons CacheDir."""

    shutil.rmtree(repo / "build", ignore_errors=True)
    root = repo / ".cache" / "cad-ci" / "scons"
    if keep_cache:
        shutil.rmtree(root / "state", ignore_errors=True)
        shutil.rmtree(root / "targets", ignore_errors=True)
        shutil.rmtree(root / "run", ignore_errors=True)
    else:
        shutil.rmtree(root, ignore_errors=True)


def read_json(path: Path) -> dict:
    """Read one JSON evidence/manifest file."""

    import json

    return json.loads(path.read_text(encoding="utf-8"))
