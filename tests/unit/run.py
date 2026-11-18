import os
from pathlib import Path

repo = Path(os.environ["CAD_CI_REPO"])
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
value = (repo / "src" / "core.txt").read_text(encoding="utf-8").strip()
assert value.startswith("core-")
(out / "unit.txt").write_text(f"unit:{value}\n", encoding="utf-8")
