#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char *capitalize_words(const char *s) {
    size_t len = strlen(s);
    char *result = (char *)malloc((len + 1) * sizeof(char));
    if (result == NULL) {
        return NULL; // Handle memory allocation failure
    }

    size_t i = 0;
    while (i < len) {
        if (i == 0 || s[i - 1] == ' ') {
            result[i] = toupper(s[i]);
        } else {
            result[i] = tolower(s[i]);
        }
        i++;
    }
    result[len] = '\0';

    return result;
}