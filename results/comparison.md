# Model and method comparison

| Tag | Model | Method | N | Pass@1 | Pass@3 | Repairs | Diff mismatch | Time (s) |
|---|---|---|---|---|---|---|---|---|
| week1 | qwen2.5-coder_3b | single shot | 8 | 6/8 | 6/8 | - | - | - |
| week1_7b | qwen2.5-coder_7b | single shot | 20 | 16/20 | 16/20 | - | - | - |
| week1_full | qwen2.5-coder_3b | single shot | 20 | 14/20 | 14/20 | - | - | - |
| week1_v2 | qwen2.5-coder_3b | single shot | 8 | 8/8 | 8/8 | - | - | - |
| week2 | qwen2.5-coder_3b | single shot | 3 | 3/3 | 3/3 | - | - | - |
| week2_nosigs | qwen2.5-coder_3b | single shot | 3 | 1/3 | 1/3 | - | - | - |
| week4 | qwen2.5-coder_3b | fix loop | 20 | 14/20 | 14/20 | 0 | - | 876.7 |
| week4_7b | qwen2.5-coder_7b | fix loop | 20 | 13/20 | 15/20 | 2 | - | 27394.4 |
| week4_7b_v2 | qwen2.5-coder_7b | fix loop | 20 | 14/20 | 16/20 | 2 | 1 | 2431.6 |
| week4_test | qwen2.5-coder_3b | fix loop | 20 | 14/20 | 14/20 | 0 | - | 1080.9 |
| week4_v2 | qwen2.5-coder_3b | fix loop | 20 | 14/20 | 14/20 | 0 | - | 1052.8 |
| week4_v3 | qwen2.5-coder_3b | fix loop | 20 | 14/20 | 14/20 | 0 | 3 | 900.8 |
| week6_deepseek | deepseek-coder_6.7b | fix loop | 20 | 7/20 | 11/20 | 4 | - | 5840.7 |

## Failure categories (single-shot runs)

**week1 / qwen2.5-coder_3b**: ? 8
**week1_7b / qwen2.5-coder_7b**: crash 2, undeclared 1, wrong_output 1
**week1_full / qwen2.5-coder_3b**: wrong_output 2, undeclared 1, buffer_overflow 1, implicit_decl 1, crash 1
**week1_v2 / qwen2.5-coder_3b**: ? 8
**week2_nosigs / qwen2.5-coder_3b**: ? 3

## Differential testing

| Tag | Model | Agree | Mismatch | Skipped |
|---|---|---|---|---|
| week4_7b_v2 | qwen2.5-coder_7b | 14 | 1 | 3 |
| week4_v3 | qwen2.5-coder_3b | 12 | 3 | 3 |
