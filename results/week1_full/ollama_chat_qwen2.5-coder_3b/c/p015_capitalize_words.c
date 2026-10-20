#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *capitalize_words(const char *s) {
    if (s == NULL) return NULL;

    size_t len = strlen(s);
    char *result = (char *)malloc(len + 1);
    if (result == NULL) return NULL;

    char *result_ptr = result;
    const char *word_start = s;
    while (*word_start) {
        if (isspace(*word_start)) {
            *result_ptr = *word_start;
            result_ptr++;
            word_start++;
        } else {
            while (word_start < s + len && !isspace(*word_start)) {
                *result_ptr = tolower(*word_start);
                result_ptr++;
                word_start++;
            }
            *result_ptr = toupper(*word_start);
            result_ptr++;
            word_start++;
        }
    }
    *result_ptr = '\0';

    return result;
}