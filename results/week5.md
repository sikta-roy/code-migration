# Week 5: differential testing

Hypothesis generates random inputs. Each one runs through the Python original and
the compiled C translation, and the outputs are compared. The C signature is parsed
automatically to work out argument and return types, so 17 of 20 problems need no
extra setup; the 3 struct-based ones are skipped and reported.

## Results on translations that already passed the hand-written tests

| Model | Agree | Mismatch | Skipped | Does not compile |
|---|---|---|---|---|
| qwen2.5-coder:3b | 12 | 3 | 3 | 2 |
| qwen2.5-coder:7b | 14 | 1 | 3 | 2 |

## The three bugs, all missed by the 20 hand-written tests

**p006_fib, input 93 — both models**
python 12200160415121876738, C -6246583658587674878.
Python integers are unbounded; long long overflows above about 9.2e18. The hand
test only checked fib(50), which fits. Not a model mistake: Python arbitrary
precision has no C equivalent. Any faithful translation needs bignum or a
documented range limit.

**p014_is_palindrome, input "00" — 3b only**
Python true, C false. Digits are alphanumeric in Python's isalnum; the C version
only handled letters. 7b got this right.

**p015_capitalize_words, input "00" — 3b only**
Heap buffer overflow caught by AddressSanitizer on a two-character input. The
hand-written test passed this same file.

Hypothesis shrank every failure to a minimal input: 93, "00", "00".

## Why this matters
These files compiled, produced no warnings, had no cppcheck findings, and passed
every hand-written test. Only running both versions on random inputs exposed them.
Hand-written tests check the cases the author thought of; the overflow at fib(93)
is exactly the case nobody thinks of.

## Limits
- 3 of 20 signatures are not supported: structs (word_count, point_distance) and a
  caller-filled array (char_freq). These need per-type harness code.
- 50 inputs per problem. More inputs would likely find more.
- Inputs are bounded (ints -1000..1000, strings <= 25 chars) to keep runs fast,
  so some overflow and size bugs are out of reach by construction.
