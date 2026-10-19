"""Week 6: gather every run under results/ into one table, and draw the charts."""
import argparse
import csv
from collections import Counter
from pathlib import Path

ROOT = Path("results")
ap = argparse.ArgumentParser()
ap.add_argument("--no-charts", action="store_true")
ap.add_argument("--out", default="results/comparison.md")
args = ap.parse_args()


def read(path):
    return list(csv.DictReader(open(path))) if path.exists() else []


def short(model):
    return model.replace("ollama_chat_", "").replace("ollama_", "")


runs = []
for tag_dir in sorted(ROOT.glob("*")):
    if not tag_dir.is_dir():
        continue
    for model_dir in sorted(tag_dir.glob("*")):
        if not model_dir.is_dir():
            continue
        rec = {"tag": tag_dir.name, "model": short(model_dir.name), "kind": None}

        check = read(model_dir / "c" / "check.csv") or read(model_dir / "files" / "check.csv")
        fix = read(model_dir / "fix" / "summary.csv")
        diff = (read(model_dir / "c" / "difftest.csv")
                or read(model_dir / "fix" / "difftest.csv"))

        if fix:
            rec["kind"] = "fix loop"
            rec["n"] = len(fix)
            rec["pass1"] = sum(r["fixed_on"] == "1" for r in fix)
            rec["passN"] = sum(r["ok"] == "True" for r in fix)
            rec["repairs"] = rec["passN"] - rec["pass1"]
            rec["calls"] = sum(int(r["attempts"]) for r in fix)
            rec["seconds"] = round(sum(float(r["seconds"]) for r in fix), 1)
            rec["cost"] = round(sum(float(r["cost_usd"]) for r in fix), 4)
            rec["api_errors"] = sum(r.get("api_error") == "True" for r in fix)
        elif check:
            rec["kind"] = "single shot"
            rec["n"] = len(check)
            rec["compiled"] = sum(r["compiled"] == "True" for r in check)
            rec["passN"] = sum(int(r["total"]) > 0 and r["passed"] == r["total"]
                               for r in check)
            rec["pass1"] = rec["passN"]
            rec["cats"] = Counter(r.get("category", "?") for r in check
                                  if r.get("category") != "pass")
        else:
            continue

        if diff:
            rec["diff_ok"] = sum(r["status"] == "ok" for r in diff)
            rec["diff_bad"] = sum(r["status"] == "mismatch" for r in diff)
            rec["diff_skip"] = sum(r["status"] == "skipped" for r in diff)
        runs.append(rec)

if not runs:
    raise SystemExit("nothing found under results/ - run a checker first")

lines = ["# Model and method comparison", "",
         "| Tag | Model | Method | N | Pass@1 | Pass@3 | Repairs | Diff mismatch | Time (s) |",
         "|---|---|---|---|---|---|---|---|---|"]
for r in runs:
    n = r.get("n", 0)
    lines.append(
        f"| {r['tag']} | {r['model']} | {r['kind']} | {n} | "
        f"{r.get('pass1', '')}/{n} | {r.get('passN', '')}/{n} | "
        f"{r.get('repairs', '-')} | {r.get('diff_bad', '-')} | {r.get('seconds', '-')} |")

lines += ["", "## Failure categories (single-shot runs)", ""]
for r in runs:
    if not r.get("cats"):
        continue
    lines.append(f"**{r['tag']} / {r['model']}**: " +
                 ", ".join(f"{k} {v}" for k, v in r["cats"].most_common()))
lines.append("")

with_diff = [r for r in runs if "diff_bad" in r]
if with_diff:
    lines += ["## Differential testing", "",
              "| Tag | Model | Agree | Mismatch | Skipped |", "|---|---|---|---|---|"]
    for r in with_diff:
        lines.append(f"| {r['tag']} | {r['model']} | {r['diff_ok']} | "
                     f"{r['diff_bad']} | {r['diff_skip']} |")
    lines.append("")

Path(args.out).write_text("\n".join(lines))
print("\n".join(lines))
print(f"\nwrote {args.out}")

if args.no_charts:
    raise SystemExit

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    raise SystemExit("matplotlib not installed: pip install matplotlib")

charts = ROOT / "charts"
charts.mkdir(exist_ok=True)

fixruns = [r for r in runs if r["kind"] == "fix loop"]
if fixruns:
    labels = [f"{r['model']}\n{r['tag']}" for r in fixruns]
    x = range(len(fixruns))
    w = 0.38
    fig, ax = plt.subplots(figsize=(1.9 * len(fixruns) + 3, 4.2))
    ax.bar([i - w / 2 for i in x], [r["pass1"] for r in fixruns], w,
           label="pass@1 (no repair)", color="#9bb8d3")
    ax.bar([i + w / 2 for i in x], [r["passN"] for r in fixruns], w,
           label="pass@3 (with repair)", color="#1f4e79")
    for i, r in enumerate(fixruns):
        if r["repairs"]:
            ax.annotate(f"+{r['repairs']}", (i + w / 2, r["passN"]),
                        ha="center", va="bottom", fontsize=9, color="#1b7f3b")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel(f"problems passing (of {fixruns[0]['n']})")
    ax.set_title("Self-fixing loop: before and after repair")
    ax.legend(); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(charts / "fix_loop.png", dpi=150); plt.close(fig)

single = [r for r in runs if r.get("cats")]
if single:
    names = sorted({k for r in single for k in r["cats"]})
    fig, ax = plt.subplots(figsize=(1.7 * len(single) + 4, 4.2))
    bottom = [0] * len(single)
    cmap = plt.get_cmap("tab20")
    for j, name in enumerate(names):
        vals = [r["cats"].get(name, 0) for r in single]
        ax.bar(range(len(single)), vals, 0.55, bottom=bottom,
               label=name, color=cmap(j % 20))
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_xticks(range(len(single)))
    ax.set_xticklabels([f"{r['model']}\n{r['tag']}" for r in single], fontsize=8)
    ax.set_ylabel("failures")
    ax.set_title("What goes wrong, by category")
    ax.legend(fontsize=7, ncol=2); ax.grid(axis="y", alpha=0.3)
    fig.tight_layout(); fig.savefig(charts / "failures.png", dpi=150); plt.close(fig)

layer = {"compiler / static": 0, "sanitizer or test run": 0, "differential testing": 0}
COMPILE_CATS = {"undeclared", "implicit_decl", "redefinition", "type_error",
                "syntax_error", "missing_symbol", "other_compile_error"}
for r in runs:
    for k, v in (r.get("cats") or {}).items():
        if k in COMPILE_CATS:
            layer["compiler / static"] += v
        else:
            layer["sanitizer or test run"] += v
    layer["differential testing"] += r.get("diff_bad", 0)
if sum(layer.values()):
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.barh(list(layer), list(layer.values()),
            color=["#9bb8d3", "#4a7fb5", "#1f4e79"])
    for i, v in enumerate(layer.values()):
        ax.text(v + 0.1, i, str(v), va="center", fontsize=9)
    ax.set_xlabel("bugs caught")
    ax.set_title("Each verification layer catches what the last one missed")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout(); fig.savefig(charts / "layers.png", dpi=150); plt.close(fig)

print(f"charts in {charts}/")
