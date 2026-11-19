import os
import time
from pathlib import Path

time.sleep(5)
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "done.txt").write_text("late\n", encoding="utf-8")
