#include <stdlib.h>
#include <ctype.h>
#include <string.h>

char *capitalize_words(const char *s) {
    size_t len = strlen(s);
    char *result = malloc(len + 1);
    bool capitalize = true;

    for (size_t i = 0; i < len; i++) {
        if (capitalize && isalpha(s[i])) {
            result[i] = toupper(s[i]);
            capitalize = false;
        } else {
            result[i] = tolower(s[i]);
        }

        if (s[i] == ' ') {
            capitalize = true;
        }
    }

    result[len] = '\0';
    return result;
}