# Week 2: multi-function files

Model: ollama_chat/qwen2.5-coder:3b. 3 files: stats (3 chained functions),
shapes (2 classes with methods), pipeline (4-step call chain).

## Pipeline
Tree-sitter splits the file into top-level functions and classes. A call graph
orders them so dependencies come first. Each unit is translated on its own, with
the already-translated prototypes passed as context. The snippets are then merged:
includes hoisted and deduped, each typedef kept once, prototypes written at the top.

## Results

| Run | Signatures given | Files compiled | Files fully passing |
|---|---|---|---|
| week2 | yes | 3/3 | 3/3 |
| week2_nosigs | no | 1/3 | 1/3 |

Only `stats` survives without signatures. `shapes` and `pipeline` fail.

## The interesting failure: shapes.py without signatures

The model produced correct C. The struct is right and the distance math is right.
But it chose a pointer API:

    double point_distance(const Point *p1, const Point *p2);

while the test calls it by value:

    double point_distance(Point a, Point b);

Nothing is wrong with the code. The interface simply does not match, so the
translation is unusable. Correct logic plus an invented API equals a broken result.

## Findings
1. The model re-wrote dependencies it was told to call, causing "redefinition"
   errors. Fixed in the assembler: first definition of each function wins.
   Prompting alone did not stop it.
2. Passing already-translated prototypes through the "signature" field made the
   model treat them as a required signature and invent a wrong out_len parameter.
   Split into a separate "context" field.
3. Prototypes at the top of the merged file remove the "used before declared"
   failure seen in Week 1 (p009_sort_asc).
4. The 3/3 headline depends on the benchmark handing over the exact C signature,
   including the class-to-struct mapping. Without it, 1/3.

## Implication for the rest of the project
API choice is a separate problem from code generation. Either the tool fixes the
signature (as our benchmark does), or verification must compare against whatever
API the model invented. We chose fixed signatures, which keeps the benchmark
measurable but hides this failure mode. Both numbers are reported above.

## Still open
- Only 3 files, all small. Bigger files are untested.
- Classes are mapped by the given signature, not discovered by the tool.
