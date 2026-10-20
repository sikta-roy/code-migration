#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>

char *most_common_word(const char *text) {
    // Convert text to lowercase and split into words
    char *lower_text = strdup(text);
    for (char *c = lower_text; *c; c++) {
        *c = tolower(*c);
    }
    char *word = strtok(lower_text, " ");
    char *best_word = NULL;
    size_t best_count = 0;

    // Count occurrences of each word
    while (word) {
        size_t count = 1;
        char *next_word = strtok(NULL, " ");
        while (next_word && strcmp(word, next_word) == 0) {
            count++;
            next_word = strtok(NULL, " ");
        }
        if (count > best_count) {
            best_count = count;
            best_word = word;
        }
        word = next_word;
    }

    // Free the lowercase text
    free(lower_text);

    // Return the best word
    return best_word ? strdup(best_word) : NULL;
}