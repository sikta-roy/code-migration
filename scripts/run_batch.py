"""Translate every problem into each target language.
Usage: python scripts/run_batch.py --model ollama/qwen2.5-coder:7b --to java cpp c --tag week1"""
import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, "src")
from migrate import translate, LANGS

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--to", nargs="+", default=["c"], choices=LANGS)
p.add_argument("--tag", default="week1")
p.add_argument("--problems", default="benchmarks/problems.jsonl")
a = p.parse_args()

probs = [json.loads(l) for l in open(a.problems)]
root = Path("results") / a.tag / a.model.replace("/", "_").replace(":", "_")
rows = []
for tgt in a.to:
    out = root / tgt
    out.mkdir(parents=True, exist_ok=True)
    for prob in probs:
        r = translate(prob["python"], "python", tgt, a.model, prob.get(f"{tgt}_signature"))
        (out / f"{prob['id']}{LANGS[tgt]['ext']}").write_text(r.code)
        rows.append({"id": prob["id"], "target": tgt, "ok": r.error is None,
                     "seconds": r.seconds, "in_tok": r.input_tokens, "out_tok": r.output_tokens,
                     "cost_usd": r.cost_usd, "error": r.error or ""})
        print(f"[{tgt}] {prob['id']}: {'ok' if r.error is None else 'FAIL'} ({r.seconds}s)")

root.mkdir(parents=True, exist_ok=True)
with open(root / "summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print(f"Saved to {root}")
