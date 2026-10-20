#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include <math.h>

int *rolling_max(const int *l, size_t n, size_t *out_len) {
    if (n == 0) {
        *out_len = 0;
        return NULL;
    }

    int *out = malloc(n * sizeof(int));
    if (out == NULL) {
        *out_len = 0;
        return NULL;
    }

    int best = l[0];
    out[0] = best;

    for (size_t i = 1; i < n; i++) {
        best = l[i] > best ? l[i] : best;
        out[i] = best;
    }

    *out_len = n;
    return out;
}