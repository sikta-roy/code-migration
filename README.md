<h1 align="center">🔄 LLM Code Migration</h1>

<p align="center">
  <b>Translate Python into Java, C++ and C using Large Language Models — then check if the result really works.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LiteLLM-any_model-FF69B4?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Ollama-local_&_free-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/status-in_progress-orange?style=for-the-badge" />
</p>

---

## 📌 What is this?

Moving old code to a new language by hand is slow and easy to get wrong. This project asks an LLM to do the translation, and then **tests the output** instead of just trusting it.

For every translated file we measure:
- ✅ **Does it compile?**
- 🧪 **Does it pass the tests?**
- 🧠 **Is it memory-safe?** (C code is built with AddressSanitizer + UndefinedBehaviorSanitizer)
- ⏱️ **How long did it take, how many tokens, how much did it cost?**

So we can compare different models fairly on the same problems.

## ✨ Features

- **Python → Java / C++ / C** from one command
- **Works with any model** through [LiteLLM](https://github.com/BerriAI/litellm) — local Ollama models (free), OpenAI or Anthropic
- **Language rules in the prompt** — e.g. C code must use `pointer + length` for lists and return `malloc`'d arrays with an `out_len`
- **Exact signatures** — each benchmark can pin the target function signature so tests always match
- **Batch runs** save every output file plus a `summary.csv` (time, tokens, cost, errors)
- **C checker** compiles with strict warnings and sanitizers, runs the tests and reports compile rate and pass rate
- **Easy to extend** — add a new language in `languages.py`, nothing else changes

## 🗂️ Project Structure

```
code-migration/
├── src/migrate/
│   ├── interface.py      # shared contract: TranslationResult, VerifyResult
│   ├── languages.py      # per-language settings and rules
│   ├── prompts.py        # system + user prompt builder
│   └── translator.py     # calls the LLM, extracts code, tracks cost
├── scripts/
│   ├── translate_one.py  # translate a single file
│   ├── run_batch.py      # translate all benchmark problems
│   └── check_c.py        # compile + test translated C files
├── benchmarks/
│   ├── problems.jsonl    # problems with Python code, C signature and C tests
│   └── sample.py
├── tests/                # pytest unit tests
├── results/              # outputs of each run (git-ignored)
└── .env.example
```

## ⚙️ Setup

```bash
git clone https://github.com/sikta-roy/code-migration.git
cd code-migration

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env              # add only the API keys you use
ollama pull qwen2.5-coder:7b      # free local model (default)
```

The C checker also needs `gcc`.

## 🚀 Usage

**Translate one file**
```bash
python scripts/translate_one.py benchmarks/sample.py --to java
```

**Translate all benchmark problems**
```bash
python scripts/run_batch.py --model ollama/qwen2.5-coder:7b --to java cpp c --tag week1
```
Outputs go to `results/<tag>/<model>/<language>/`.

**Check the C translations**
```bash
python scripts/check_c.py results/week1/ollama_qwen2.5-coder_7b/c
```
Prints compile rate and fully-passing count, and saves a `check.csv`.

**Run unit tests**
```bash
pytest
```

> ⚠️ `check_c.py` runs LLM-generated code on your machine. Only use it with trusted benchmarks until it is moved into Docker.

## 🧩 Adding a Benchmark Problem

Each line in `benchmarks/problems.jsonl` needs:

| Field | Meaning |
|---|---|
| `id` | unique name, e.g. `p004_reverse` |
| `python` | the original Python code |
| `c_signature` | the exact C function signature to use |
| `c_test` | a C `main()` that prints `passed/total` |

## 🛣️ Roadmap

- [x] Translation for Java, C++ and C
- [x] Batch runs with cost and token tracking
- [x] C compile + test checker with sanitizers
- [ ] `verify()` for Java and C++
- [ ] Run checks safely inside Docker
- [ ] Bigger benchmark set
- [ ] Compare more models side by side

## 👥 Team

Built by a team of two — one side owns **translation**, the other owns **verification**. Both meet at `src/migrate/interface.py`.

---

<p align="center">Made with 💖 by <a href="https://github.com/sikta-roy">Sikta Roy</a></p>
