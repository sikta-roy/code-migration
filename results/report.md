# Results so far

| Tag | Model | Set | N | Compiled | All tests pass |
|---|---|---|---|---|---|
| week1 | ollama_chat_qwen2.5-coder_3b | c | 8 | 6/8 (75%) | 6/8 (75%) |
| week1_7b | ollama_chat_qwen2.5-coder_7b | c | 20 | 19/20 (95%) | 16/20 (80%) |
| week1_full | ollama_chat_qwen2.5-coder_3b | c | 20 | 18/20 (90%) | 14/20 (70%) |
| week1_v2 | ollama_chat_qwen2.5-coder_3b | c | 8 | 8/8 (100%) | 8/8 (100%) |
| week2 | ollama_chat_qwen2.5-coder_3b | files | 3 | 3/3 (100%) | 3/3 (100%) |
| week2_nosigs | ollama_chat_qwen2.5-coder_3b | files | 3 | 1/3 (33%) | 1/3 (33%) |

## Failure buckets

**week1 / ollama_chat_qwen2.5-coder_3b / c**
- ?: 8

**week1_7b / ollama_chat_qwen2.5-coder_7b / c**
- crash: 2 _(runtime only: compiler and static analysis miss this)_
- undeclared: 1
- wrong_output: 1 _(runtime only: compiler and static analysis miss this)_

**week1_full / ollama_chat_qwen2.5-coder_3b / c**
- wrong_output: 2 _(runtime only: compiler and static analysis miss this)_
- undeclared: 1
- buffer_overflow: 1 _(runtime only: compiler and static analysis miss this)_
- implicit_decl: 1
- crash: 1 _(runtime only: compiler and static analysis miss this)_

**week1_v2 / ollama_chat_qwen2.5-coder_3b / c**
- ?: 8

**week2_nosigs / ollama_chat_qwen2.5-coder_3b / files**
- ?: 3

## Why running the code matters

- failures the compiler catches: 22
- failures only running the code catches: 7
