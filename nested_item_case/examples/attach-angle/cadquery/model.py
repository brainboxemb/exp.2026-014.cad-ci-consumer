"""Synthetic nested consumer B."""

from __future__ import annotations

import os
from pathlib import Path


repo = Path(os.environ["CAD_CI_REPO"])
output = Path(os.environ["CAD_CI_OUTPUT"])
output.mkdir(parents=True, exist_ok=True)
(output / "result.txt").write_text(
    "cadquery:" + (repo / "shared.txt").read_text(encoding="utf-8"),
    encoding="utf-8",
)
