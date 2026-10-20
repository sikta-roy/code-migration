"""Week 7: explicit Python-to-C mapping rules.

Switched on with --rules so the same benchmark runs with and without them.
Everything here comes from a failure we actually observed.
"""

PY_TO_C_MAPPING = """
Python features that have no C equivalent. Follow these mappings exactly:
- raise / except: C has no exceptions. Return an int status (0 ok, -1 error) and
  write the real result through an out-pointer, or return a sentinel the caller
  can check. Never call exit() or abort().
- class: map to a struct holding the fields, plus free functions that take a
  pointer to it as the first argument (name_init, name_method).
- yield / generator: map to a state struct plus a next function returning bool,
  writing the value through an out-pointer and returning false when exhausted.
- default argument: C has none. Write the full function, plus a second wrapper
  function that supplies the default.
- None: for a missing value return bool false and leave the out-pointer alone,
  or return a documented sentinel. Do not return 0 to mean "not found".
- list comprehension: write an explicit loop into a malloc'd buffer and report
  the length through size_t *out_len.
- Python int is unbounded; C int is not. Use long long where values can grow,
  and never cast a possibly negative value to size_t.
- Python creates a fresh value each call. If the caller supplies an output
  buffer, initialise all of it before use.
- strdup is POSIX, not C11. Use malloc + strcpy.
- Declare every helper function before it is used, including qsort comparators.
"""
