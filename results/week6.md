# Week 6: model comparison

| Model | pass@1 | pass@3 | repairs | extra calls | notes |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | 14/20 | 14/20 | 0 | 12 | repairs nothing |
| qwen2.5-coder:7b | 14/20 | 16/20 | 2 | 9 | ~5x slower than 3b |
| deepseek-coder:6.7b | 7/20 | 16/20 | 9 | 18 | 2 API errors remain |

## Main finding
First-try quality and repair ability are different skills.

deepseek-coder translates worst on the first attempt (7/20) and ends level with
qwen-7b (16/20) by repairing 9 problems, including p009_sort_asc, which neither
qwen model ever fixed. qwen-3b translates twice as well on the first try and
repairs nothing at all.

So "which model is best" depends on whether a repair loop is in the pipeline.
Ranking models on single-shot pass rate alone would pick the wrong one here.

## Cost of that repair
deepseek is slow: 18 extra calls and runs of 100-1700s per problem, against
roughly 30s for qwen-3b. Strong repair is paid for in time.

## Caveats
- 2 of 20 deepseek problems still hit API errors, so its numbers may be 1-2 low.
- All models run locally via Ollama, so cost is zero and only time varies.
- An earlier deepseek run (week6_deepseek) had 9 API errors and is invalid.
  Use week6_deepseek_v2.

## Still open
- Differential testing has not been run on the deepseek output.
- results/ holds superseded runs (week4, week4_v2, week4_test, week6_deepseek)
  that clutter compare.py. Keep week1_full, week1_7b, week4_v3, week4_7b_v2,
  week6_deepseek_v2.
- week1 and week1_v2 predate the category column and show "? 8".
