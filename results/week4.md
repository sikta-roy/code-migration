# Week 4: self-fixing loop

Loop: translate -> compile and run tests -> send the error back -> retry (max 3).
Repair has its own prompt and code path, not the translation prompt.
Feedback mode "compile": compiler and sanitizer errors go back in full; a wrong
answer is reported only as "compiles but gives wrong results", with no test detail.

## Result: repair works, but only on the larger model

| Model | pass@1 | pass@2 | pass@3 | repairs | extra calls |
|---|---|---|---|---|---|
| qwen2.5-coder:3b | 14/20 | 14/20 | 14/20 | 0 | 12 |
| qwen2.5-coder:7b | 14/20 | 16/20 | 16/20 | 2 | 9 |

7b repaired p002_close and p014_is_palindrome. p014 is the notable one: it was told
only that the output was wrong, with no detail, and still found the bug.

3b repaired nothing. Given 'int_cmp' undeclared or implicit declaration of 'strdup'
three times over, it regenerated slightly different code each attempt and repeated
the same mistake. gcc even suggests the correct replacement for strdup; the model
ignored it.

Self-repair is not a free win from adding a loop. It needs a model able to read an
error and act on it, and there is a capability threshold between 3b and 7b.

## Cost of repair
9 extra model calls bought 2 fixes on 7b, and 12 extra calls bought 0 on 3b.
7b is also far slower per call: p017 took 458s against 40s on 3b.

## Still failing on 7b
p009_sort_asc (comparator undeclared), p017_word_count and p020_most_common_word
(strdup, which is POSIX not C11), p018_char_freq (output array never zeroed).
All four are the same class: C rules that have no Python equivalent.

## Three bugs found while building this
1. The first loop wrapped the repair request inside the translation prompt, so the
   model received "Translate this Python code to C" followed by a broken-C report
   inside a ```python fence. Repair now has its own prompt. Naive retry gained 0.
2. Six "failures" were verification timeouts, not bad translations. The 10s limit
   was too short while Ollama held memory and AddressSanitizer was starting.
   Raised to 60s; the same code verified fine when run alone.
3. One run showed p009 taking 23,642s (6.5 hours) from a stalled model call, and
   another problem failed on a LiteLLM API error counted as a translation failure.
   Added a 180s per-call timeout and an api_error column so infrastructure failures
   are no longer scored as model failures.

Each of these would have silently corrupted the numbers.
