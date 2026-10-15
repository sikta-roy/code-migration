"""Per-language settings. Add a new language here, nothing else needs to change."""
LANGS = {
    "python": {"name": "Python", "fence": "python", "ext": ".py"},
    "java": {
        "name": "Java", "fence": "java", "ext": ".java",
        "rules": "- Put everything in `public class Solution` as static methods.\n"
                 "- No main() method. No package line.\n"
                 "- Use only java.util / java.lang.",
    },
    "cpp": {
        "name": "C++ (C++17)", "fence": "cpp", "ext": ".cpp",
        "rules": "- Use C++17 and the standard library only.\n"
                 "- Free functions, no main().\n"
                 "- Use std::vector, std::string, std::unordered_map, etc.",
    },
    "c": {
        "name": "C (C11)", "fence": "c", "ext": ".c",
        "rules": "- Use C11 and the standard library only. No main().\n"
                 "- For lists, pass a pointer plus a length (e.g. `const double *arr, size_t n`).\n"
                 "- If returning an array, return a malloc'd pointer and write its length to an `size_t *out_len` parameter.\n"
                 "- Include EVERY header you use. Common ones: <stdlib.h> for malloc/free/abs, "
                 "<string.h> for strlen/strcmp, <ctype.h> for tolower/isalpha, "
                 "<math.h> for fabs/sqrt, <stdbool.h> for bool, <stddef.h> for size_t.\n"
                 "- Use `bool` from <stdbool.h>.",
    },
}
