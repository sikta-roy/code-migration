#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

bool is_palindrome(const char *s) {
    size_t len = strlen(s);
    char *clean = (char *)malloc(len + 1);
    if (!clean) return false;

    size_t j = 0;
    for (size_t i = 0; i < len; ++i) {
        if (isalnum((unsigned char)s[i])) {
            clean[j++] = tolower((unsigned char)s[i]);
        }
    }
    clean[j] = '\0';

    bool result = true;
    size_t n = j;
    for (size_t i = 0; i < n / 2; ++i) {
        if (clean[i] != clean[n - i - 1]) {
            result = false;
            break;
        }
    }

    free(clean);
    return result;
}