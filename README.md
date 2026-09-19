# LLM Code Migration: Python → Java, C++, C

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # add keys
ollama pull qwen2.5-coder:7b   # free local model
```

## Run
```bash
python scripts/translate_one.py benchmarks/sample.py --to java
python scripts/run_batch.py --model ollama/qwen2.5-coder:7b --to java cpp c --tag week1
pytest
```

Shared interface: see `src/migrate/interface.py`.

## Python → C (current focus)
```bash
python scripts/run_batch.py --model ollama/qwen2.5-coder:7b --to c --tag week1
python scripts/check_c.py results/week1/ollama_qwen2.5-coder_7b/c
```
Each problem in `benchmarks/problems.jsonl` needs: `id`, `python`, `c_signature`, `c_test`
(a C `main()` that prints `passed/total`).
