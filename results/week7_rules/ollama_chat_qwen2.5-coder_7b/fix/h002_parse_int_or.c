#include <stdlib.h>
#include <ctype.h>
#include <limits.h>

int parse_int_or(const char *s, int fallback) {
    if (s == NULL) {
        return fallback;
    }

    char *end;
    long long value = strtoll(s, &end, 10);

    if (end == s || *end != '\0') {
        return fallback;
    }

    if (value < INT_MIN || value > INT_MAX) {
        return fallback;
    }

    return (int)value;
}