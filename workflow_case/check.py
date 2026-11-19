"""Verify reusable workflow environment and GHCR authentication."""

from __future__ import annotations

import json
import os
from pathlib import Path


EXPECTED = "repository-config"


def ghcr_authentication_available() -> bool:
    """Return whether Docker has a GHCR auth entry without reading its value."""

    config_path = Path.home() / ".docker" / "config.json"
    if not config_path.is_file():
        return False

    value = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        return False

    auths = value.get("auths")
    return isinstance(auths, dict) and "ghcr.io" in auths


def main() -> int:
    """Fail unless released workflow setup reaches the consumer command."""

    actual = os.environ.get("ACCEPTANCE_MARKER")
    if actual != EXPECTED:
        raise RuntimeError(
            f"ACCEPTANCE_MARKER must be {EXPECTED!r}, found {actual!r}"
        )

    if not ghcr_authentication_available():
        raise RuntimeError(
            "reusable workflow must authenticate Docker to ghcr.io "
            "before running the consumer command"
        )

    output = Path(os.environ["CAD_CI_OUTPUT"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "result.txt").write_text(
        "reusable workflow executed caller item; "
        "ghcr authentication available\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
