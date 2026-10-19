"""Week 5: differential testing. Python original vs C translation on random inputs."""
import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, "src")
from hypothesis import given, settings, strategies as st, HealthCheck
from migrate.difftest import (Harness, parse_signature, encode_input,
                              format_expected, same, DiffReport,
                              INT, DOUBLE, STR, INT_ARR, DOUBLE_ARR, BOOL)

p = argparse.ArgumentParser()
p.add_argument("dir")
p.add_argument("--examples", type=int, default=50)
p.add_argument("--problems", default="benchmarks/problems.jsonl")
a = p.parse_args()

TEXT = st.text(alphabet=st.characters(min_codepoint=32, max_codepoint=126), max_size=25)
NUM = st.integers(min_value=-1000, max_value=1000)
FLT = st.floats(min_value=-1e4, max_value=1e4, allow_nan=False, allow_infinity=False)

STRATEGY = {
    INT: NUM, BOOL: st.booleans(), DOUBLE: FLT, STR: TEXT,
    INT_ARR: st.lists(NUM, max_size=10),
    DOUBLE_ARR: st.lists(FLT, max_size=8),
}


def python_fn(problem, name):
    ns = {}
    exec(problem["python"], ns)
    if name in ns:
        return ns[name]
    fns = [v for k, v in ns.items() if callable(v) and not k.startswith("_")]
    return fns[-1] if fns else None


def check_one(problem, c_code, max_examples):
    sig = parse_signature(problem["c_signature"])
    if sig is None:
        return DiffReport(supported=False, error="signature shape not supported")
    fn = python_fn(problem, sig.name)
    if fn is None:
        return DiffReport(supported=False, error="no python function found")

    h = Harness(c_code, sig)
    if h.compile_error:
        h.close()
        return DiffReport(supported=True, error="does not compile")

    rep = DiffReport(supported=True)
    strat = st.tuples(*[STRATEGY[t] for t in sig.args])

    @settings(max_examples=max_examples, deadline=None,
              suppress_health_check=list(HealthCheck))
    @given(strat)
    def prop(values):
        values = list(values)
        rep.ran += 1
        try:
            expected = format_expected(sig, fn(*values))
        except Exception:
            return
        got, err = h.run(encode_input(sig, values))
        if err:
            rep.mismatches.append((values, expected, f"CRASH: {err[:120]}"))
            raise AssertionError(f"crash on {values!r}")
        if not same(sig, expected, got):
            rep.mismatches.append((values, expected, got))
            raise AssertionError(f"{values!r}: python={expected!r} c={got!r}")

    try:
        prop()
    except Exception:
        pass
    finally:
        h.close()
    return rep


rows = []
src = Path(a.dir)
for line in open(a.problems):
    prob = json.loads(line)
    f = src / f"{prob['id']}.c"
    if not f.exists():
        continue
    rep = check_one(prob, f.read_text(), a.examples)
    if not rep.supported:
        print(f"{prob['id']:24} skipped ({rep.error})")
        rows.append({"id": prob["id"], "status": "skipped", "ran": 0, "detail": rep.error})
        continue
    if rep.error:
        print(f"{prob['id']:24} {rep.error}")
        rows.append({"id": prob["id"], "status": rep.error, "ran": 0, "detail": ""})
        continue
    if rep.mismatches:
        vals, exp, got = rep.mismatches[-1]
        kind = "HANG" if "HANG" in str(got) else ("CRASH" if "CRASH" in str(got) else "MISMATCH")
        print(f"{prob['id']:24} {kind} after {rep.ran} inputs")
        print(f"{'':26}input    {vals!r}")
        print(f"{'':26}python   {exp!r}")
        print(f"{'':26}c        {got!r}")
        rows.append({"id": prob["id"], "status": kind.lower(), "ran": rep.ran,
                     "detail": f"input={vals!r} python={exp!r} c={got!r}"[:300]})
    else:
        print(f"{prob['id']:24} ok ({rep.ran} inputs)")
        rows.append({"id": prob["id"], "status": "ok", "ran": rep.ran, "detail": ""})

n_ok = sum(r["status"] == "ok" for r in rows)
n_bad = sum(r["status"] in ("mismatch", "hang", "crash") for r in rows)
n_skip = sum(r["status"] == "skipped" for r in rows)
print(f"\nagree: {n_ok}   mismatch: {n_bad}   skipped: {n_skip}   of {len(rows)} files")

out = src / "difftest.csv"
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"wrote {out}")
