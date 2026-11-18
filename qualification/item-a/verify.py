import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
built = (out / "built.txt").read_text(encoding="utf-8").strip()
assert "integration:unit:core-v1" in built
(out / "verified.txt").write_text("pass\n", encoding="utf-8")
