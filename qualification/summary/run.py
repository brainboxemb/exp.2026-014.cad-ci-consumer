"""Create one synthetic fan-in summary from two completed item outputs."""

from __future__ import annotations

import json
import os
from pathlib import Path


repo = Path(os.environ["CAD_CI_REPO"])
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)

lines = []
for item in ("item-a", "item-b"):
    root = repo / "build" / "qualification" / item
    state = json.loads((root / "item.json").read_text(encoding="utf-8"))
    if state.get("status") != "pass":
        raise RuntimeError(f"{item} is not complete")
    verified = (root / "verified.txt").read_text(encoding="utf-8").strip()
    lines.append(f"{item}:{verified}")

(out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
