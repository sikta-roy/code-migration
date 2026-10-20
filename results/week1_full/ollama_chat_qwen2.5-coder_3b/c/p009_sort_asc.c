#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>

int *sort_asc(const int *l, size_t n, size_t *out_len) {
    int *sorted = malloc(n * sizeof(int));
    if (!sorted) {
        *out_len = 0;
        return NULL;
    }

    for (size_t i = 0; i < n; i++) {
        sorted[i] = l[i];
    }

    qsort(sorted, n, sizeof(int), (int (*)(const void *, const void *))int_cmp);

    *out_len = n;
    return sorted;
}

int int_cmp(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}