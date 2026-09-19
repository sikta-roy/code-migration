"""Usage: python scripts/translate_one.py file.py --to java [--model MODEL]"""
import argparse, sys
sys.path.insert(0, "src")
from migrate import translate, LANGS

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("--from", dest="src", default="python", choices=LANGS)
p.add_argument("--to", dest="tgt", required=True, choices=LANGS)
p.add_argument("--model", default=None)
a = p.parse_args()

r = translate(open(a.file).read(), a.src, a.tgt, a.model)
if r.error:
    sys.exit(f"Error: {r.error}")
print(r.code)
print(f"\n// model={r.model} time={r.seconds}s tokens={r.input_tokens}+{r.output_tokens} cost=${r.cost_usd:.5f}",
      file=sys.stderr)
