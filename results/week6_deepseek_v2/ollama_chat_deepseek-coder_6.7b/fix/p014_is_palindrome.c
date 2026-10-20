#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool is_palindrome(const char *s) {
    size_t len = strlen(s);
    char *clean = malloc(len + 1);
    size_t j = 0;

    for (size_t i = 0; i < len; i++) {
        char c = tolower(s[i]);
        if (isalnum(c)) {
            clean[j++] = c;
        }
    }

    clean[j] = '\0';

    for (size_t i = 0; i < j / 2; i++) {
        if (clean[i] != clean[j - i - 1]) {
            free(clean);
            return false;
        }
    }

    free(clean);
    return true;
}