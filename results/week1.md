# Week 1 baseline

3 problems (p001_add, p002_close, p003_positive), Python -> C.

| Model | Compiled | All tests pass | Avg time |
|---|---|---|---|
| ollama_chat/qwen2.5-coder:3b | 3/3 | 3/3 | 29s |

Notes:
- 7b model crashed in WSL (low memory); 3b used instead.
- litellm needs the `ollama_chat/` prefix, not `ollama/`.
- Small sample. Real baseline comes after all 20 problems are written.
