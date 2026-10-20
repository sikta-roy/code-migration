# Week 7: hard language features and prompt tuning

7 new problems covering what C does not have: exceptions (2), classes with mutable
state, generators, default arguments, None returns, nested comprehensions.
Model: qwen2.5-coder:7b, fix loop, 3 attempts, compile-mode feedback.

## A/B: explicit Python-to-C mapping rules in the prompt

| Run | Rules | pass@1 | pass@3 | repaired |
|---|---|---|---|---|
| week7_norules_v2 | off | 5/7 | 5/7 | none |
| week7_rules_v3 | ON | 5/7 | 6/7 | h002_parse_int_or |

## Main finding: the rules help repair, not generation

pass@1 is 5/7 in both runs. The mapping rules changed nothing about the first
translation. The gain appears at attempt 2: without the rules the model failed
h002_parse_int_or three times; with them it fixed it on the second try.

So a prompt rule is not only an instruction for writing code. It is also context
the model uses when reading an error. That is a different mechanism from the Week 1
header rule, which lifted first-attempt compile rate from 75% to 100%.

## What passes without any help
Classes (struct + functions), generators (state struct + next), None returns
(bool + out-pointer), and nested comprehensions all passed on the first attempt
with no mapping rules. Given a fixed C signature, the model infers the mapping.
The signature carries most of the information; the prose rules add little.

## h005_greet_default: fails in every configuration

Default arguments. The model writes both functions correctly, including the
wrapper. The bug is arithmetic:

    size_t total_len = greeting_len + 2 + name_len + 1;  // +2 for ", " and +1 for '\0'

It needs 4 extra bytes: ", " (2), "!" (1), '\0' (1). It allocates 3. The final
strcat writes one byte past the buffer. The comment shows the model counted the
separator and the terminator and forgot the "!" it writes two lines later.

Three attempts, with the full AddressSanitizer heap-buffer-overflow report fed
back each time, did not fix it. Same result with and without the mapping rules.
This is not a missing-knowledge failure; it is an arithmetic slip the model cannot
see even when told exactly where it is.

## A tool bug found here
Compile-mode feedback was replacing every runtime error with "the code compiles
but gives wrong results", including sanitizer output. That muted the most
informative message we had. Sanitizer reports are diagnostics, not the answer key,
so they now pass through while test comparisons stay hidden. The h005 numbers
above are from after the fix; they did not change, which makes the finding
stronger rather than weaker.

## Feature-by-feature result

| Feature | Problem | Result |
|---|---|---|
| exception -> status code | h001_safe_divide | pass, attempt 1 |
| exception -> fallback | h002_parse_int_or | needs the rules, then attempt 2 |
| class -> struct + functions | h003_counter | pass, attempt 1 |
| generator -> state struct | h004_squares_gen | pass, attempt 1 |
| default arg -> wrapper fn | h005_greet_default | fails everywhere (malloc off-by-one) |
| None -> bool + out-pointer | h006_find_index | pass, attempt 1 |
| comprehension -> loop | h007_flatten_evens | pass, attempt 1 |
