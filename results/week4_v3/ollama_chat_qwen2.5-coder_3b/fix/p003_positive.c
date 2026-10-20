#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>

int *get_positive(const int *l, size_t n, size_t *out_len) {
    size_t count = 0;
    for (size_t i = 0; i < n; i++) {
        if (l[i] > 0) {
            count++;
        }
    }
    int *result = malloc(count * sizeof(int));
    if (result == NULL) {
        *out_len = 0;
        return NULL;
    }
    size_t j = 0;
    for (size_t i = 0; i < n; i++) {
        if (l[i] > 0) {
            result[j++] = l[i];
        }
    }
    *out_len = count;
    return result;
}