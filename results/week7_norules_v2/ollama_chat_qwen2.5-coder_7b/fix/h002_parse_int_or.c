#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

int parse_int_or(const char *s, int fallback) {
    char *end;
    long val = strtol(s, &end, 10);
    if (*end == '\0' && val >= INT_MIN && val <= INT_MAX) {
        return (int)val;
    } else {
        return fallback;
    }
}