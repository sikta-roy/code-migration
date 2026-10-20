# Model and method comparison

| Tag | Model | Method | N | Pass@1 | Pass@3 | Repairs | Diff mismatch | Time (s) |
|---|---|---|---|---|---|---|---|---|
| week1_7b | qwen2.5-coder_7b | single shot | 20 | 16/20 | 16/20 | - | - | - |
| week1_full | qwen2.5-coder_3b | single shot | 20 | 14/20 | 14/20 | - | - | - |
| week4_7b_v2 | qwen2.5-coder_7b | fix loop | 20 | 14/20 | 16/20 | 2 | 1 | 2431.6 |
| week4_v3 | qwen2.5-coder_3b | fix loop | 20 | 14/20 | 14/20 | 0 | 3 | 900.8 |
| week6_deepseek_v2 | deepseek-coder_6.7b | fix loop | 20 | 7/20 | 16/20 | 9 | 1 | 10147.3 |
| week7_norules | qwen2.5-coder_7b | fix loop | 7 | 5/7 | 5/7 | 0 | - | 101.9 |
| week7_norules_v2 | qwen2.5-coder_7b | fix loop | 7 | 5/7 | 5/7 | 0 | - | 113.5 |
| week7_rules | qwen2.5-coder_7b | fix loop | 7 | 5/7 | 6/7 | 1 | - | 106.5 |
| week7_rules_v2 | qwen2.5-coder_7b | fix loop | 7 | 5/7 | 6/7 | 1 | - | 110.5 |
| week7_rules_v3 | qwen2.5-coder_7b | fix loop | 7 | 5/7 | 6/7 | 1 | - | 126.9 |

## Failure categories (single-shot runs)

**week1_7b / qwen2.5-coder_7b**: crash 2, undeclared 1, wrong_output 1
**week1_full / qwen2.5-coder_3b**: wrong_output 2, undeclared 1, buffer_overflow 1, implicit_decl 1, crash 1

## Differential testing

| Tag | Model | Agree | Mismatch | Skipped |
|---|---|---|---|---|
| week4_7b_v2 | qwen2.5-coder_7b | 14 | 1 | 3 |
| week4_v3 | qwen2.5-coder_3b | 12 | 3 | 3 |
| week6_deepseek_v2 | deepseek-coder_6.7b | 12 | 1 | 3 |
