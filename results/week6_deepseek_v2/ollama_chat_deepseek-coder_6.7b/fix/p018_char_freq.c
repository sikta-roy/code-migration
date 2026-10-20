#include <ctype.h>
#include <string.h>

void char_freq(const char *s, int counts[26]) {
    for (int i = 0; i < 26; i++) {
        counts[i] = 0;
    }

    for (size_t i = 0; i < strlen(s); i++) {
        char c = tolower(s[i]);
        if (isalpha(c)) {
            counts[c - 'a']++;
        }
    }
}