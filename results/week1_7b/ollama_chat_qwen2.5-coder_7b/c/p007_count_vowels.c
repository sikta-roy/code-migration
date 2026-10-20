#include <ctype.h>
#include <stddef.h>

int count_vowels(const char *s) {
    int count = 0;
    while (*s) {
        char c = tolower(*s);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
        s++;
    }
    return count;
}