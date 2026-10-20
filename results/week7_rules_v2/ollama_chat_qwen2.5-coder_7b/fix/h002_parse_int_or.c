#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <limits.h>

int parse_int_or(const char *s, int fallback) {
    char *end;
    long long val = strtoll(s, &end, 10);
    if (end == s || *end != '\0') {
        return fallback;
    }
    if (val < INT_MIN || val > INT_MAX) {
        return fallback;
    }
    return (int)val;
}