#include <stdlib.h>
#include <string.h>

char *greet(const char *name, const char *greeting) {
    size_t name_len = strlen(name);
    size_t greeting_len = strlen(greeting);
    size_t total_len = greeting_len + 2 + name_len + 1; // +2 for ", " and +1 for '\0'

    char *result = (char *)malloc(total_len);
    if (result == NULL) {
        return NULL; // Handle memory allocation failure
    }

    snprintf(result, total_len, "%s, %s!", greeting, name);
    return result;
}

char *greet_default(const char *name) {
    return greet(name, "Hello");
}