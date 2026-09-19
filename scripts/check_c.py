"""Compile + run tests for translated C files.
Usage: python scripts/check_c.py results/week1/<model>/c
NOTE: runs code on your machine. Move this into Docker in Week 3."""
import csv, json, subprocess, sys, tempfile
from pathlib import Path

HEADERS = "#include <stdbool.h>\n#include <stddef.h>\n"
src_dir = Path(sys.argv[1])
probs = {json.loads(l)["id"]: json.loads(l) for l in open("benchmarks/problems.jsonl")}
rows = []

for pid, prob in probs.items():
    f = src_dir / f"{pid}.c"
    row = {"id": pid, "compiled": False, "warnings": 0, "passed": 0, "total": 0, "error": ""}
    if not f.exists():
        row["error"] = "missing"; rows.append(row); continue
    with tempfile.TemporaryDirectory() as tmp:
        full = Path(tmp) / "t.c"
        full.write_text(HEADERS + f.read_text() + "\n\n" + prob["c_test"])
        exe = Path(tmp) / "t"
        c = subprocess.run(["gcc", "-std=c11", "-Wall", "-Wextra", "-O0",
                            "-fsanitize=address,undefined", str(full), "-o", str(exe), "-lm"],
                           capture_output=True, text=True)
        row["warnings"] = c.stderr.count("warning:")
        if c.returncode != 0:
            row["error"] = c.stderr.strip()[:300]; rows.append(row); continue
        row["compiled"] = True
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=5)
            last = (r.stdout.strip().splitlines() or ["0/0"])[-1]
            row["passed"], row["total"] = map(int, last.split("/"))
            if r.returncode != 0 and r.stderr:
                row["error"] = r.stderr.strip()[:300]   # e.g. memory bug from sanitizer
        except subprocess.TimeoutExpired:
            row["error"] = "timeout"
        except ValueError:
            row["error"] = "bad test output"
    rows.append(row)
    print(f"{pid}: compiled={row['compiled']} tests={row['passed']}/{row['total']} {row['error'][:60]}")

n = len(rows)
print(f"\nCompile rate: {sum(r['compiled'] for r in rows)}/{n}")
print(f"Fully passing: {sum(r['total'] > 0 and r['passed'] == r['total'] for r in rows)}/{n}")
with open(src_dir / "check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
