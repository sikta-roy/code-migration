#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stddef.h>

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

    int *result = (int *)malloc(n * sizeof(int));
    if (result == NULL) {
        free(seen);
        *out_len = 0;
        return NULL;
    }

    int count = 0;
    for (size_t i = 0; i < n; i++) {
        bool found = false;
        for (size_t j = 0; j < count; j++) {
            if (seen[j] == l[i]) {
                found = true;
                break;
            }
        }
        if (!found) {
            seen[count++] = l[i];
            result[count - 1] = l[i];
        }
    }

    *out_len = count;
    free(seen);
    return result;
}