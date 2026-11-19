import os
from pathlib import Path

item = Path(__file__).parent
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
text = "".join(
    path.read_text(encoding="utf-8")
    for path in sorted((item / "input").glob("*.txt"))
)
(out / "built.txt").write_text(text, encoding="utf-8")
