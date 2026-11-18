import os
from pathlib import Path

repo = Path(os.environ["CAD_CI_REPO"])
item_path = Path(os.environ["CAD_CI_ITEM_PATH"])
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
integration = (repo / "build" / "examples" / "example-a" / "integration.txt").read_text(encoding="utf-8").strip()
source = (item_path / "input.txt").read_text(encoding="utf-8").strip()
(out / "built.txt").write_text(f"{source}|{integration}\n", encoding="utf-8")
