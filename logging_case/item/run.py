import os
from pathlib import Path
import time

print("logging-consumer-start", flush=True)
time.sleep(1.0)
out = Path(os.environ["CAD_CI_OUTPUT"])
out.mkdir(parents=True, exist_ok=True)
(out / "result.txt").write_text("ok\n", encoding="utf-8")
print("logging-consumer-end", flush=True)
