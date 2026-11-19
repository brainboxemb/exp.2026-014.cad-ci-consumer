import os
from pathlib import Path

out = Path(os.environ["CAD_CI_OUTPUT"])
assert (out / "built.txt").read_text(encoding="utf-8")
(out / "verified.txt").write_text("verified\n", encoding="utf-8")
