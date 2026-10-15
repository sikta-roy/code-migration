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

## Root causes (week1_full)

| Problem | Type | Cause |
|---|---|---|
| p009_sort_asc | compile | comparator used before it is declared (C needs forward declaration) |
| p017_word_count | compile | used strdup(), which is POSIX, not C11 |
| p020_most_common_word | compile | (see check.csv) |
| p015_capitalize_words | crash | buffer overflow, caught only by AddressSanitizer at runtime |
| p014_is_palindrome | wrong | 3/4, logic bug on mixed alphanumeric input |
| p018_char_freq | wrong | 2/3, logic bug |

Key point: p015 compiled with zero warnings and zero cppcheck issues. Only running
it under AddressSanitizer exposed the bug. Compilation alone is not verification.
