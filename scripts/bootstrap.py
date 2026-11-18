#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dependencies.repos"
TARGET = ROOT / "ext" / "cad-ci"


def read_dependency() -> tuple[str, str]:
    text = MANIFEST.read_text(encoding="utf-8")
    block = re.search(r"(?ms)^  cad-ci:\s*\n(.*?)(?=^  [\w-]+:|\Z)", text)
    if not block:
        raise RuntimeError("dependencies.repos has no cad-ci entry")
    url = re.search(r"(?m)^    url:\s*(\S+)\s*$", block.group(1))
    version = re.search(r"(?m)^    version:\s*([0-9a-f]{40})\s*$", block.group(1))
    if not url or not version:
        raise RuntimeError("cad-ci requires a Git URL and exact commit SHA")
    return url.group(1), version.group(1)


def run(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def main() -> int:
    url, wanted = read_dependency()
    TARGET.parent.mkdir(parents=True, exist_ok=True)

    if (TARGET / ".git").is_dir():
        dirty = run("git", "-C", str(TARGET), "status", "--porcelain", "--untracked-files=no")
        if dirty:
            raise RuntimeError("ext/cad-ci has tracked local changes")
        run("git", "-C", str(TARGET), "remote", "set-url", "origin", url)
        current = run("git", "-C", str(TARGET), "rev-parse", "HEAD")
        if current != wanted:
            subprocess.run(["git", "-C", str(TARGET), "fetch", "--quiet", "origin", wanted], check=True)
            subprocess.run(["git", "-C", str(TARGET), "checkout", "--quiet", "--detach", wanted], check=True)
    else:
        if TARGET.exists():
            shutil.rmtree(TARGET)
        subprocess.run(["git", "clone", "--quiet", "--no-checkout", url, str(TARGET)], check=True)
        subprocess.run(["git", "-C", str(TARGET), "checkout", "--quiet", "--detach", wanted], check=True)

    actual = run("git", "-C", str(TARGET), "rev-parse", "HEAD")
    if actual != wanted:
        raise RuntimeError(f"cad-ci revision mismatch: expected {wanted}, found {actual}")
    print(f"cad-ci ready at {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
