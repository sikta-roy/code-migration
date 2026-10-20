#include <stdlib.h>
#include <string.h>

char *reverse_string(const char *s) {
    size_t len = strlen(s);
    char *reversed = malloc(len + 1);
    for (size_t i = 0; i < len; i++) {
        reversed[i] = s[len - i - 1];
    }
    reversed[len] = '\0';
    return reversed;
}