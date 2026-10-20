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

## Differential testing on deepseek output (added later)

| Model | Agree | Mismatch | Skipped | Does not compile |
|---|---|---|---|---|
| qwen2.5-coder:3b | 12 | 3 | 3 | 2 |
| qwen2.5-coder:7b | 14 | 1 | 3 | 2 |
| deepseek-coder:6.7b | 12 | 1 | 3 | 2 |

deepseek repaired 9 problems, far more than any other model, and its repaired code
holds up under random inputs about as well as the others. The repairs are real
fixes, not code shaped to pass the specific hand-written tests.

### New bugs found
- p006_fib with input -1: hangs forever. A negative n cast into a size_t loop
  counter wraps to a huge number. All three models produce this, so it is a
  systematic Python-to-C gap rather than one model's mistake.
- p015_capitalize_words with "0A": python "0a", C "0A". Python's str.capitalize()
  lowercases the rest of the word; the C version only uppercases the first letter.
- p016_longest_word with "0A": segfault (AddressSanitizer DEADLYSIGNAL) on a
  two-character input.

### Note on comparing numbers
week1_7b reads 16/20 in comparison.md but was 14/20 when first run on the laptop.
The difference is the compiler: the Docker sandbox gcc accepts a file the laptop
gcc rejected. Use container numbers throughout the final report and say so.
