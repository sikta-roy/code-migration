#include <stdlib.h>
#include <string.h>

char *longest_word(const char *s) {
    if (s == NULL || *s == '\0') {
        return NULL;
    }

    const char *word = s;
    const char *best = s;
    size_t best_len = 0;

    while (*s != '\0') {
        if (*s == ' ') {
            size_t word_len = s - word;
            if (word_len > best_len) {
                best = word;
                best_len = word_len;
            }
            word = s + 1;
        }
        s++;
    }

    size_t word_len = s - word;
    if (word_len > best_len) {
        best = word;
        best_len = word_len;
    }

    char *result = (char *)malloc(best_len + 1);
    if (result == NULL) {
        return NULL;
    }

    strncpy(result, best, best_len);
    result[best_len] = '\0';

    return result;
}