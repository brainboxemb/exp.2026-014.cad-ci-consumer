"""Create one synthetic fan-in summary through the public CI library API."""

from cad_ci import current_context


context = current_context()
lines = []
for item_id in ("qualification-item-a", "qualification-item-b"):
    dependency = context.dependency(item_id)
    verified = dependency.output("verified.txt").read_text(
        encoding="utf-8"
    ).strip()
    lines.append(f"{item_id.removeprefix('qualification-')}:{verified}")

context.output.mkdir(parents=True, exist_ok=True)
(context.output / "summary.txt").write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8",
)
