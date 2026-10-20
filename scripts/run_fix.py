"""Week 4: translate with a self-fixing loop and record attempt-by-attempt results."""
import argparse, csv, json, sys
from pathlib import Path
sys.path.insert(0, "src")
from migrate.fixloop import translate_with_fixes
from migrate.verify_c import verify_c
from migrate.translator import translate, repair
from migrate.rules import PY_TO_C_MAPPING

p = argparse.ArgumentParser()
p.add_argument("--model", required=True)
p.add_argument("--tag", default="week4")
p.add_argument("--attempts", type=int, default=3)
p.add_argument("--feedback", choices=["compile", "test"], default="compile")
p.add_argument("--problems", default="benchmarks/problems.jsonl")
p.add_argument("--rules", action="store_true",
               help="add the explicit Python-to-C mapping rules to the prompt")
a = p.parse_args()

out_dir = Path("results") / a.tag / a.model.replace("/", "_").replace(":", "_") / "fix"
out_dir.mkdir(parents=True, exist_ok=True)


RULES = PY_TO_C_MAPPING if a.rules else None


def tr(code, src, tgt, model, signature=None, context=None):
    return translate(code, src, tgt, model, signature=signature,
                     context=context, extra_rules=RULES)


def rp(code, error, target, model, signature=None):
    return repair(code, error, target, model, signature=signature, extra_rules=RULES)


def make_verify(c_test):
    def v(code, _test=None):
        res = verify_c(code, c_test)
        if a.feedback == "compile" and res.compiled and not res.ok:
            # Sanitizer output is a runtime diagnostic, not the answer key, so it
            # goes back like a compiler error. Only the test comparison is hidden.
            sanitizer = ("AddressSanitizer" in res.error or "runtime error:" in res.error
                         or "LeakSanitizer" in res.error)
            if not sanitizer:
                res.error = "the code compiles but gives wrong results"
        elif a.feedback == "compile" and res.ok:
            res.error = ""
        return res
    return v


rows = []
for line in open(a.problems):
    prob = json.loads(line)
    r = translate_with_fixes(prob["python"], prob["c_test"], model=a.model,
                             signature=prob.get("c_signature"),
                             max_attempts=a.attempts, verify=make_verify(prob["c_test"]),
                             translate_fn=tr, repair_fn=rp)
    (out_dir / f"{prob['id']}.c").write_text(r.code)
    (out_dir / f"{prob['id']}.attempts.json").write_text(json.dumps(
        [{"n": x.n, "ok": x.ok, "error": x.error[:500], "seconds": x.seconds}
         for x in r.attempts], indent=1))
    api_fail = any(not x.code and x.error for x in r.attempts)
    rows.append({"id": prob["id"], "ok": r.ok, "api_error": api_fail,
                 "attempts": r.n_attempts,
                 "fixed_on": r.fixed_on or "", "seconds": r.seconds,
                 "cost_usd": round(r.cost_usd, 5),
                 "first_error": (r.attempts[0].error.splitlines() or [""])[0][:120]})
    print(f"{prob['id']}: {'PASS' if r.ok else 'fail'} "
          f"after {r.n_attempts} attempt(s) ({r.seconds}s)")

n = len(rows)
at1 = sum(r["fixed_on"] == 1 for r in rows)
at2 = sum(r["fixed_on"] in (1, 2) for r in rows)
at3 = sum(bool(r["ok"]) for r in rows)
print(f"\nfeedback mode: {a.feedback}   mapping rules: {'ON' if a.rules else 'off'}")
api = sum(bool(r["api_error"]) for r in rows)
print(f"pass@1: {at1}/{n}   pass@2: {at2}/{n}   pass@{a.attempts}: {at3}/{n}")
if api:
    print(f"WARNING: {api} problem(s) hit an API error, not a translation failure")
print(f"extra model calls spent on repairs: {sum(r['attempts'] for r in rows) - n}")

with open(out_dir / "summary.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"Saved to {out_dir}")
