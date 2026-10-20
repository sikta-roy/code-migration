#include <stdlib.h>
#include <stdbool.h>

bool contains(int *arr, size_t len, int target) {
    for (size_t i = 0; i < len; i++) {
        if (arr[i] == target) {
            return true;
        }
    }
    return false;
}

int *unique(const int *l, size_t n, size_t *out_len) {
    int *seen = malloc(n * sizeof(int));
    *out_len = 0;
    for (size_t i = 0; i < n; i++) {
        if (!contains(seen, *out_len, l[i])) {
            seen[(*out_len)++] = l[i];
        }
    }
    seen = realloc(seen, *out_len * sizeof(int));
    return seen;
}