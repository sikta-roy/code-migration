#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>

typedef struct {
    char word[32];
    int count;
    struct WordCount *next;
} WordCount;

WordCount *word_count(const char *text, size_t *out_len) {
    if (text == NULL) {
        *out_len = 0;
        return NULL;
    }

    // Convert text to lowercase and split into words
    char *lower_text = strdup(text);
    for (char *p = lower_text; *p; p++) {
        *p = tolower((unsigned char)*p);
    }
    char *word = strtok(lower_text, " ");
    size_t word_count = 0;

    // Count words
    while (word != NULL) {
        WordCount *wc = (WordCount *)malloc(sizeof(WordCount));
        wc->count = 1;
        wc->word[0] = '\0';
        strncat(wc->word, word, sizeof(wc->word) - 1);

        // Check if the word is already in the list
        WordCount *current = NULL;
        for (current = lower_text; current != NULL; current = current->next) {
            if (strcmp(current->word, wc->word) == 0) {
                current->count++;
                free(wc);
                break;
            }
        }

        // If the word is not in the list, add it
        if (current == NULL) {
            wc->next = lower_text;
            lower_text = wc;
            word_count++;
        }

        word = strtok(NULL, " ");
    }

    // Free the allocated memory
    free(lower_text);

    // Set the output length
    *out_len = word_count;

    return lower_text;
}