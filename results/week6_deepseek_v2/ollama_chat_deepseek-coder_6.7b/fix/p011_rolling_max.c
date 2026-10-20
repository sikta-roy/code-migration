#include <stdlib.h>
#include <limits.h>

int* rolling_max(const int *l, size_t n, size_t *out_len) {
    int *out = (int*)malloc(n * sizeof(int));
    int best = INT_MIN;
    for (size_t i = 0; i < n; i++) {
        best = (best > l[i]) ? best : l[i];
        out[i] = best;
    }
    *out_len = n;
    return out;
}