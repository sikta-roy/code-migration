#include <ctype.h>
#include <string.h>

int count_vowels(const char *s) {
    int count = 0;
    for (int i = 0; i < strlen(s); i++) {
        char c = tolower(s[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
    }
    return count;
}