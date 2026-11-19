"""Verify that the reusable workflow executes the caller consumer context."""

from __future__ import annotations

import os
from pathlib import Path


EXPECTED = "repository-config"


def main() -> int:
    """Fail unless repository CI configuration reaches the consumer command."""

    actual = os.environ.get("ACCEPTANCE_MARKER")
    if actual != EXPECTED:
        raise RuntimeError(
            f"ACCEPTANCE_MARKER must be {EXPECTED!r}, found {actual!r}"
        )

    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "result.txt").write_text(
        "reusable workflow executed caller item\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
