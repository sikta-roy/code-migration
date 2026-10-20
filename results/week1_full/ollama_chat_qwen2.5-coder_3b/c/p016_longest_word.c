#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

char *longest_word(const char *s) {
    if (!s || *s == '\0') {
        return NULL;
    }

    const char *word_start = s;
    const char *best_start = s;
    size_t best_len = 0;

    while (*s) {
        if (isspace(*s)) {
            if (s - word_start > best_len) {
                best_len = s - word_start;
                best_start = word_start;
            }
            word_start = s + 1;
        }
        s++;
    }

    if (s - word_start > best_len) {
        best_len = s - word_start;
        best_start = word_start;
    }

    char *result = malloc(best_len + 1);
    if (!result) {
        return NULL;
    }

    strncpy(result, best_start, best_len);
    result[best_len] = '\0';

    return result;
}