#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool is_palindrome(const char *s) {
    size_t len = strlen(s);
    char *clean = (char *)malloc(len * sizeof(char));
    if (!clean) {
        return false; // Memory allocation failed
    }

    size_t clean_len = 0;
    for (size_t i = 0; i < len; ++i) {
        char c = s[i];
        if (isalnum(c)) {
            clean[clean_len++] = tolower(c);
        }
    }

    bool result = (clean_len == 0) || (clean_len == 1 && clean[0] == tolower(s[0]));
    for (size_t i = 0; i < clean_len / 2; ++i) {
        if (clean[i] != clean[clean_len - 1 - i]) {
            result = false;
            break;
        }
    }

    free(clean);
    return result;
}