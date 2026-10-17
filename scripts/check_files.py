"""Week 2: compile + test whole translated C files.
Usage: python scripts/check_files.py results/week2/<model>/files"""
import csv, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, "src")
from migrate.errors import classify, RUNTIME_ONLY

HEADERS = "#include <stdbool.h>\n#include <stddef.h>\n"
src_dir = Path(sys.argv[1])
specs = {json.loads(l)["id"]: json.loads(l) for l in open("benchmarks/files.jsonl")}
rows = []

for fid, spec in specs.items():
    f = src_dir / f"{fid}.c"
    row = {"id": fid, "compiled": False, "warnings": 0, "passed": 0, "total": 0, "error": ""}
    if not f.exists():
        row["error"] = "missing"; rows.append(row); continue
    with tempfile.TemporaryDirectory() as tmp:
        full = Path(tmp) / "t.c"
        full.write_text(HEADERS + f.read_text() + "\n\n" + spec["c_test"])
        exe = Path(tmp) / "t"
        c = subprocess.run(["gcc", "-std=c11", "-Wall", "-Wextra", "-O0",
                            "-fsanitize=address,undefined", str(full), "-o", str(exe), "-lm"],
                           capture_output=True, text=True)
        row["warnings"] = c.stderr.count("warning:")
        if c.returncode != 0:
            row["error"] = c.stderr.strip().replace("\n", " | ")[:200]
            rows.append(row); continue
        row["compiled"] = True
        try:
            r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=10)
            last = (r.stdout.strip().splitlines() or ["0/0"])[-1]
            row["passed"], row["total"] = map(int, last.split("/"))
            if r.returncode != 0 and r.stderr:
                row["error"] = r.stderr.strip().replace("\n", " | ")[:200]
        except subprocess.TimeoutExpired:
            row["error"] = "timeout"
        except ValueError:
            row["error"] = "bad test output"
    rows.append(row)
    print(f"{fid}: compiled={row['compiled']} tests={row['passed']}/{row['total']} "
          f"warn={row['warnings']} {row['error'][:60]}")

for r in rows:
    r["category"] = classify(r["error"], r["compiled"], r["passed"], r["total"])

n = len(rows)
print(f"\nFiles compiled: {sum(r['compiled'] for r in rows)}/{n}")
print(f"Files fully passing: {sum(r['total'] > 0 and r['passed'] == r['total'] for r in rows)}/{n}")
from collections import Counter
cats = Counter(r["category"] for r in rows)
print("\nFailure buckets:")
for name, k in cats.most_common():
    if name != "pass":
        flag = "  (compiler/static analysis cannot catch this)" if name in RUNTIME_ONLY else ""
        print(f"  {name}: {k}{flag}")

with open(src_dir / "check.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
