#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    char word[32];
    int count;
} WordCount;

int compare_strings(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

WordCount* word_count(const char *text, size_t *out_len) {
    char *copy = strdup(text);
    char *token = strtok(copy, " ");
    WordCount *counts = NULL;
    size_t i = 0;

    while (token != NULL) {
        bool found = false;
        for (size_t j = 0; j < i; j++) {
            if (strcmp(counts[j].word, token) == 0) {
                counts[j].count++;
                found = true;
                break;
            }
        }
        if (!found) {
            counts = realloc(counts, (i + 1) * sizeof(WordCount));
            strncpy(counts[i].word, token, 31);
            counts[i].word[31] = '\0';
            counts[i].count = 1;
            i++;
        }
        token = strtok(NULL, " ");
    }

    *out_len = i;
    free(copy);
    return counts;
}