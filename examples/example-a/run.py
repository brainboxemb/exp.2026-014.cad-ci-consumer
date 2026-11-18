import os
from pathlib import Path

repo = Path(os.environ["CAD_CI_REPO"])
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
unit = (repo / "build" / "tests" / "unit" / "unit.txt").read_text(encoding="utf-8").strip()
(out / "integration.txt").write_text(f"integration:{unit}\n", encoding="utf-8")
