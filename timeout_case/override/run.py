import os
import time
from pathlib import Path

time.sleep(1.2)
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "done.txt").write_text("ok\n", encoding="utf-8")
