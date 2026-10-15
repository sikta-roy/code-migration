"""Translate a whole Python file (many functions) into one C file.
Usage: python scripts/translate_file.py myfile.py --model ollama_chat/qwen2.5-coder:3b"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, "src")
from migrate import translate, LANGS
from migrate.parser import parse_python, order_units
from migrate.assemble import assemble_c, prototypes

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("--to", dest="tgt", default="c", choices=LANGS)
p.add_argument("--model", default=None)
p.add_argument("--out", default=None)
a = p.parse_args()

code = Path(a.file).read_text()
preamble, units = parse_python(code)
units = order_units(units)
print(f"found {len(units)} units: " + ", ".join(f"{u.name}({u.kind})" for u in units))

snippets, done_sigs = [], []
for u in units:
    ctx = "\n".join(done_sigs) if done_sigs else None
    r = translate(u.code, "python", a.tgt, a.model, context=ctx)
    if r.error:
        print(f"  {u.name}: FAIL {r.error[:80]}")
        continue
    print(f"  {u.name}: ok ({r.seconds}s)")
    snippets.append(r.code)
    if a.tgt == "c":
        done_sigs += prototypes(r.code)

out = Path(a.out or Path(a.file).with_suffix(LANGS[a.tgt]["ext"]).name)
out.write_text(assemble_c(snippets) if a.tgt == "c" else "\n\n".join(snippets))
print(f"wrote {out}")
