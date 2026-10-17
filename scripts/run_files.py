"""Week 2: translate whole multi-function Python files into one C file each.
Usage: python scripts/run_files.py --model ollama_chat/qwen2.5-coder:3b --tag week2"""
import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, "src")
from migrate import translate
from migrate.parser import parse_python, order_units
from migrate.assemble import assemble_c, prototypes

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--tag", default="week2")
p.add_argument("--files", default="benchmarks/files.jsonl")
p.add_argument("--no-sigs", action="store_true",
               help="do not give the model the expected C signatures")
a = p.parse_args()

out_dir = Path("results") / a.tag / a.model.replace("/", "_").replace(":", "_") / "files"
out_dir.mkdir(parents=True, exist_ok=True)
rows = []

for line in open(a.files):
    spec = json.loads(line)
    code = Path(spec["path"]).read_text()
    _, units = parse_python(code)
    units = order_units(units)
    snippets, done, secs, dup = [], [], 0.0, 0
    for u in units:
        r = translate(u.code, "python", "c", a.model,
                      signature=None if a.no_sigs else spec.get("signatures", {}).get(u.name),
                      context="\n".join(done) if done else None)
        secs += r.seconds
        if r.error:
            print(f"[{spec['id']}] {u.name}: FAIL {r.error[:60]}")
            continue
        snippets.append(r.code)
        new = prototypes(r.code)
        dup += sum(1 for n in new if n in done)
        done += [n for n in new if n not in done]
        print(f"[{spec['id']}] {u.name}: ok ({r.seconds}s)")
    (out_dir / f"{spec['id']}.c").write_text(assemble_c(snippets))
    rows.append({"id": spec["id"], "units": len(units), "redefined": dup,
                 "seconds": round(secs, 1)})

with open(out_dir / "summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"Saved to {out_dir}")
