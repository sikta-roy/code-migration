#include <stdlib.h>

int *get_positive(const int *l, size_t n, size_t *out_len) {
    size_t count = 0;
    for (size_t i = 0; i < n; ++i) {
        if (l[i] > 0) {
            ++count;
        }
    }
    *out_len = count;
    if (count == 0) {
        return NULL;
    }
    int *result = (int *)malloc(count * sizeof(int));
    if (result == NULL) {
        return NULL;
    }
    size_t j = 0;
    for (size_t i = 0; i < n; ++i) {
        if (l[i] > 0) {
            result[j++] = l[i];
        }
    }
    return result;
}