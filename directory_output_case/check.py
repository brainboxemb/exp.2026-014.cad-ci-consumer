#!/usr/bin/env python3
"""Black-box directory materialization and CacheDir restore acceptance."""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tests.support import fresh_case, remove_local_scons_state, run_tool

SOURCE = Path(__file__).resolve().parent


def main() -> int:
    repo = fresh_case(SOURCE, "directory_output_case")
    generated = repo / "build/item/generated"

    cold = run_tool("run", "--repo", str(repo))
    assert "built: directory-case:build materialization=unchanged" in cold
    assert (generated / "nested/value.txt").read_text() == "one\n"
    assert (generated / "empty").is_dir()

    current = run_tool("run", "--repo", str(repo))
    assert "current: directory-case:build materialization=unchanged" in current

    shutil.rmtree(generated)
    restored = run_tool("run", "--repo", str(repo))
    assert "current: directory-case:build materialization=restored" in restored
    assert (generated / "empty").is_dir()

    (generated / "nested/value.txt").write_text("tampered\n", encoding="utf-8")
    (generated / "extra.txt").write_text("extra\n", encoding="utf-8")
    repaired = run_tool("run", "--repo", str(repo))
    assert "current: directory-case:build materialization=repaired" in repaired
    assert (generated / "nested/value.txt").read_text() == "one\n"
    assert not (generated / "extra.txt").exists()

    remove_local_scons_state(repo, keep_cache=True)
    fresh = run_tool("run", "--repo", str(repo))
    assert "cache_restored: directory-case:build materialization=restored" in fresh
    assert (generated / "nested/value.txt").read_text() == "one\n"
    assert (generated / "empty").is_dir()

    print("directory_output_case passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
