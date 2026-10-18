# Week 4: self-fixing loop

Loop: translate -> compile and test -> send the error back -> retry (max 3).
Repair uses its own prompt and its own code path, not the translation prompt.

## Results, qwen2.5-coder:3b, 20 problems

| Feedback mode | pass@1 | pass@2 | pass@3 | extra model calls |
|---|---|---|---|---|
| compile | 14/20 | 14/20 | 14/20 | 12 |
| test | 14/20 | 14/20 | 14/20 | 12 |

The loop repaired nothing. 12 extra calls, zero gain.

## Why: the model repeats the same mistake

| Problem | Error given back, all 3 attempts |
|---|---|
| p009_sort_asc | 'int_cmp' undeclared (first use in this function) |
| p017_word_count | implicit declaration of 'strdup'; did you mean 'strcmp'? |
| p020_most_common_word | implicit declaration of 'strdup' |
| p014, p015, p018 | compiles, wrong output |

The code changes slightly between attempts (error column numbers move), so the model
is regenerating, not echoing. It simply does not use the error. gcc even suggests the
correct replacement for strdup and the model ignores it.

## Two bugs found and fixed on the way
1. The first version wrapped the repair request inside the translation prompt
   ("Translate this Python code to C: ```python This c code does not work...").
   Nested code fences, wrong language label. Repair now has its own prompt.
2. Six failures were verification TIMEOUTS, not bad translations: the 10s limit was
   too short while the Ollama model held memory and AddressSanitizer was starting up.
   Raised to 60s. The same code verified fine when run alone. This is the argument for
   running verification in Docker with its own limits, away from the model process.

## Conclusion
Self-repair is not free. It depends on the model being able to read a compiler error
and act on it, and a 3b model cannot. The loop must be re-measured on larger models
before any claim about its value.
