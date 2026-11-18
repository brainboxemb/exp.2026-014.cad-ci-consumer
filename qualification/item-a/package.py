"""Create one nested result directory for directory-output testing."""

from __future__ import annotations

import json
import os
from pathlib import Path


def main() -> int:
    """Write deterministic result files below the item-owned output directory."""

    output = Path(os.environ["CAD_CI_OUTPUT"])
    verified = (output / "verified.txt").read_text(encoding="utf-8").strip()

    results = output / "results"
    nested = results / "nested"
    nested.mkdir(parents=True, exist_ok=True)
    (results / "status.txt").write_text(
        f"{verified}\n",
        encoding="utf-8",
    )
    (nested / "provenance.json").write_text(
        json.dumps({"status": verified}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
