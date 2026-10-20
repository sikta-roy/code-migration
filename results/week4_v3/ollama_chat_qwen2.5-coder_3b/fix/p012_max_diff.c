#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>

int max_diff(const int *l, size_t n) {
    if (n == 0) {
        return 0;
    }
    int min_val = l[0];
    int max_val = l[0];
    for (size_t i = 1; i < n; i++) {
        if (l[i] < min_val) {
            min_val = l[i];
        }
        if (l[i] > max_val) {
            max_val = l[i];
        }
    }
    return max_val - min_val;
}