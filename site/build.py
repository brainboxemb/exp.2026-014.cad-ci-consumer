#!/usr/bin/env python3
"""Build the synthetic consumer site with the tool.cad.ci Pages framework."""

from __future__ import annotations

import argparse
from pathlib import Path

from cad_ci.pages import Page, build_site


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Build one small site that records the source and build commits."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--build-commit", required=True)
    parser.add_argument("--base-path", required=True)
    args = parser.parse_args()

    build_site(
        out=args.out,
        site_title="cad-ci synthetic consumer",
        pages=[
            Page(
                "index.html",
                "Consumer status",
                "<p>The synthetic build and publication flow passed.</p>",
            ),
            Page(
                "layout/index.html",
                "Repository layout",
                "<p>library tests → integration example → qualification items</p>",
            ),
        ],
        provenance={
            "schema": 1,
            "source_commit": args.source_commit,
            "build_commit": args.build_commit,
        },
        stylesheet_source=ROOT / "site" / "site.css",
        base_path=args.base_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
