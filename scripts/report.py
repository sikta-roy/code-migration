"""Week 3: one table from every run so far. Writes results/report.md"""
import csv
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, "src")
from migrate.errors import RUNTIME_ONLY

ROOT = Path("results")
runs = []

for csv_path in sorted(ROOT.glob("*/*/*/check.csv")):
    kind = csv_path.parent.name
    model = csv_path.parent.parent.name
    tag = csv_path.parent.parent.parent.name
    rows = list(csv.DictReader(open(csv_path)))
    n = len(rows)
    comp = sum(r["compiled"] == "True" for r in rows)
    full = sum(int(r["total"]) > 0 and r["passed"] == r["total"] for r in rows)
    cats = Counter(r.get("category", "?") for r in rows)
    runs.append({"tag": tag, "model": model, "kind": kind, "n": n,
                 "compiled": comp, "passed": full, "cats": cats})

if not runs:
    sys.exit("no check.csv found under results/ - run a checker first")

lines = ["# Results so far", "",
         "| Tag | Model | Set | N | Compiled | All tests pass |",
         "|---|---|---|---|---|---|"]
for r in runs:
    lines.append(f"| {r['tag']} | {r['model']} | {r['kind']} | {r['n']} | "
                 f"{r['compiled']}/{r['n']} ({100*r['compiled']//r['n']}%) | "
                 f"{r['passed']}/{r['n']} ({100*r['passed']//r['n']}%) |")

lines += ["", "## Failure buckets", ""]
for r in runs:
    bad = {k: v for k, v in r["cats"].items() if k != "pass"}
    if not bad:
        continue
    lines.append(f"**{r['tag']} / {r['model']} / {r['kind']}**")
    for name, k in sorted(bad.items(), key=lambda x: -x[1]):
        note = " _(runtime only: compiler and static analysis miss this)_" \
               if name in RUNTIME_ONLY else ""
        lines.append(f"- {name}: {k}{note}")
    lines.append("")

runtime = sum(v for r in runs for k, v in r["cats"].items() if k in RUNTIME_ONLY)
compile_time = sum(v for r in runs for k, v in r["cats"].items()
                   if k not in RUNTIME_ONLY and k != "pass")
lines += ["## Why running the code matters", "",
          f"- failures the compiler catches: {compile_time}",
          f"- failures only running the code catches: {runtime}", ""]

out = ROOT / "report.md"
out.write_text("\n".join(lines))
print("\n".join(lines))
print(f"\nwrote {out}")
