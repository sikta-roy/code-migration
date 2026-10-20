#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>

typedef struct {
    char word[32];
    int count;
} WordCount;

WordCount *word_count(const char *text, size_t *out_len) {
    const char *delimiters = " \t\n\r\f\v";
    size_t n_words = 0;
    WordCount *counts = NULL;

    // Count the number of words
    const char *token = strtok((char *)text, delimiters);
    while (token != NULL) {
        n_words++;
        token = strtok(NULL, delimiters);
    }

    // Allocate memory for the word counts
    counts = (WordCount *)malloc(n_words * sizeof(WordCount));
    if (counts == NULL) {
        *out_len = 0;
        return NULL;
    }

    // Initialize the word counts
    for (size_t i = 0; i < n_words; i++) {
        counts[i].count = 0;
        memset(counts[i].word, 0, sizeof(counts[i].word));
    }

    // Count the occurrences of each word
    token = strtok((char *)text, delimiters);
    while (token != NULL) {
        size_t len = strlen(token);
        if (len < sizeof(counts[0].word)) {
            bool found = false;
            for (size_t i = 0; i < n_words; i++) {
                if (strcmp(counts[i].word, token) == 0) {
                    counts[i].count++;
                    found = true;
                    break;
                }
            }
            if (!found) {
                for (size_t i = 0; i < n_words; i++) {
                    if (counts[i].count == 0) {
                        strcpy(counts[i].word, token);
                        counts[i].count = 1;
                        break;
                    }
                }
            }
        }
        token = strtok(NULL, delimiters);
    }

    *out_len = n_words;
    return counts;
}