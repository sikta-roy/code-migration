#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

char *reverse_string(const char *s) {
    size_t len = strlen(s);
    char *reversed = (char *)malloc(len + 1);
    if (reversed == NULL) {
        return NULL; // Handle memory allocation failure
    }
    for (size_t i = 0; i < len; i++) {
        reversed[len - 1 - i] = s[i];
    }
    reversed[len] = '\0';
    return reversed;
}