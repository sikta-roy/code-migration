#include <stdlib.h>

int *unique(const int *l, size_t n, size_t *out_len) {
    if (n == 0) {
        *out_len = 0;
        return NULL;
    }

    int *seen = (int *)malloc(n * sizeof(int));
    if (seen == NULL) {
        *out_len = 0;
        return NULL;
    }

    size_t unique_count = 0;
    for (size_t i = 0; i < n; ++i) {
        bool is_unique = true;
        for (size_t j = 0; j < unique_count; ++j) {
            if (l[i] == seen[j]) {
                is_unique = false;
                break;
            }
        }
        if (is_unique) {
            seen[unique_count++] = l[i];
        }
    }

    *out_len = unique_count;
    int *result = (int *)realloc(seen, unique_count * sizeof(int));
    if (result == NULL) {
        free(seen);
        *out_len = 0;
        return NULL;
    }

    return result;
}