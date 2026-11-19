#!/usr/bin/env python3
"""Black-box cold/current and selective-input acceptance."""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, run_tool

SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "simple_case1")

    first = run_tool("run", "--repo", str(repo))
    assert "built: simple-case:build" in first
    assert "built: simple-case:verify" in first
    assert (repo / "build/item/.cad-ci/item.json").is_file()

    second = run_tool("run", "--repo", str(repo))
    assert "current: simple-case:build" in second
    assert "current: simple-case:verify" in second

    with (repo / "item/verify.py").open("a", encoding="utf-8") as handle:
        handle.write("# verify-only change\n")
    verify_only = run_tool("run", "--repo", str(repo))
    assert "current: simple-case:build" in verify_only
    assert "built: simple-case:verify" in verify_only

    # This case proves target invalidation rather than historical cache lookup.
    shutil.rmtree(
        repo / ".cache/cad-ci/scons/cache",
        ignore_errors=True,
    )
    (repo / "item/input/b.txt").write_text("two\n", encoding="utf-8")
    membership = run_tool("run", "--repo", str(repo))
    assert "built: simple-case:build" in membership
    assert "built: simple-case:verify" in membership

    print("simple_case1 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
