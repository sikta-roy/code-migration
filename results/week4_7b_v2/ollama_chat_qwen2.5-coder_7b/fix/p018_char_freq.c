#include <ctype.h>
#include <stddef.h>

void char_freq(const char *s, int counts[26]) {
    for (size_t i = 0; s[i] != '\0'; ++i) {
        char c = tolower(s[i]);
        if (isalpha(c)) {
            counts[c - 'a']++;
        }
    }
}