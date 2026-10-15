# Week 1 baseline

8 problems, Python -> C, model: ollama_chat/qwen2.5-coder:3b (local).

| Run | Prompt | Compiled | All tests pass | Avg time |
|---|---|---|---|---|
| v1 | base C rules | 6/8 (75%) | 6/8 (75%) | 22s |
| v2 | + explicit header rule | 8/8 (100%) | 8/8 (100%) | 17s |

## v1 failures (logic correct, headers missing)
- p004_gcd: abs() without <stdlib.h>
- p007_count_vowels: tolower() without <ctype.h>, used <string.h> instead

## Fix
Added one line to the C rules: list every header you use, with the common ones
named (stdlib, string, ctype, math, stdbool, stddef). Both failures cleared.

## Notes
- 7b model crashes in WSL from low RAM; 3b used instead.
- litellm needs the `ollama_chat/` prefix, not `ollama/`.
- cppcheck reports 11 style issues on the simplest problem, so static issue count
  does not track correctness. Use it as a code-quality signal only.
