#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

typedef struct {
    char* word;
    int count;
} word_count;

bool is_word_separator(char c) {
    return c == ' ' || c == '\n' || c == '\t' || c == '.' || c == ',' || c == ';' || c == ':' || c == '!' || c == '?';
}

char* most_common_word(const char *text) {
    word_count* counts = NULL;
    size_t count_size = 0;
    const char* word_start = text;
    const char* word_end = text;
    while (*word_end) {
        if (is_word_separator(*word_end)) {
            if (word_end != word_start && *(word_end - 1) != ' ') {
                *word_end = '\0';
                for (size_t i = 0; i < count_size; i++) {
                    if (strcmp(counts[i].word, word_start) == 0) {
                        counts[i].count++;
                        *word_end = *(word_end - 1);
                        goto found;
                    }
                }
                counts = realloc(counts, (count_size + 1) * sizeof(word_count));
                counts[count_size].word = malloc(word_end - word_start + 1);
                strcpy(counts[count_size].word, word_start);
                counts[count_size].count = 1;
                count_size++;
            }
            word_start = word_end + 1;
        }
        word_end++;
    }
found:
    int best_n = 0;
    char* best = NULL;
    for (size_t i = 0; i < count_size; i++) {
        if (counts[i].count > best_n) {
            best_n = counts[i].count;
            best = counts[i].word;
        }
    }
    for (size_t i = 0; i < count_size; i++) {
        free(counts[i].word);
    }
    free(counts);
    return best;
}