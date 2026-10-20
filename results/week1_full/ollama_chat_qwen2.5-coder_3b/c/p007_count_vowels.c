#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int count_vowels(const char *s) {
    int count = 0;
    for (const char *c = s; *c != '\0'; c++) {
        char lower_c = tolower(*c);
        if (lower_c == 'a' || lower_c == 'e' || lower_c == 'i' || lower_c == 'o' || lower_c == 'u') {
            count++;
        }
    }
    return count;
}