#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

char *most_common_word(const char *text) {
    size_t len = strlen(text);
    char *lower_text = (char *)malloc(len + 1);
    if (lower_text == NULL) {
        return NULL; // Handle memory allocation failure
    }

    // Convert text to lowercase
    for (size_t i = 0; i < len; i++) {
        lower_text[i] = tolower(text[i]);
    }
    lower_text[len] = '\0';

    // Split text into words and count occurrences
    char *token = strtok(lower_text, " ");
    char **words = (char **)malloc(100 * sizeof(char *));
    size_t word_count = 0;
    size_t words_capacity = 100;
    while (token != NULL) {
        if (word_count >= words_capacity) {
            words_capacity *= 2;
            words = (char **)realloc(words, words_capacity * sizeof(char *));
            if (words == NULL) {
                free(lower_text);
                return NULL; // Handle memory allocation failure
            }
        }
        words[word_count] = strdup(token);
        if (words[word_count] == NULL) {
            free(lower_text);
            for (size_t j = 0; j < word_count; j++) {
                free(words[j]);
            }
            free(words);
            return NULL; // Handle memory allocation failure
        }
        word_count++;
        token = strtok(NULL, " ");
    }

    // Count occurrences of each word
    size_t *counts = (size_t *)calloc(word_count, sizeof(size_t));
    if (counts == NULL) {
        free(lower_text);
        for (size_t j = 0; j < word_count; j++) {
            free(words[j]);
        }
        free(words);
        return NULL; // Handle memory allocation failure
    }

    for (size_t i = 0; i < word_count; i++) {
        for (size_t j = i + 1; j < word_count; j++) {
            if (strcmp(words[i], words[j]) == 0) {
                counts[i]++;
                free(words[j]);
                words[j] = NULL;
            }
        }
    }

    // Find the most common word
    char *best = NULL;
    size_t best_n = 0;
    for (size_t i = 0; i < word_count; i++) {
        if (words[i] != NULL && counts[i] > best_n) {
            best = words[i];
            best_n = counts[i];
        }
    }

    // Free allocated memory
    for (size_t i = 0; i < word_count; i++) {
        free(words[i]);
    }
    free(words);
    free(counts);
    free(lower_text);

    return best;
}