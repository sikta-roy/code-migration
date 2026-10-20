#include <stdlib.h>
#include <string.h>

char *reverse_string(const char *s) {
    size_t len = strlen(s);
    char *result = (char *)malloc((len + 1) * sizeof(char));
    if (result == NULL) {
        return NULL; // Handle memory allocation failure
    }
    for (size_t i = 0; i < len; ++i) {
        result[i] = s[len - 1 - i];
    }
    result[len] = '\0';
    return result;
}