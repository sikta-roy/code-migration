#include <stdlib.h>
#include <stdbool.h>

int* get_positive(const int *l, size_t n, size_t *out_len) {
    int *result = (int*)malloc(n * sizeof(int));
    size_t count = 0;

    for (size_t i = 0; i < n; i++) {
        if (l[i] > 0) {
            result[count] = l[i];
            count++;
        }
    }

    *out_len = count;
    return result;
}