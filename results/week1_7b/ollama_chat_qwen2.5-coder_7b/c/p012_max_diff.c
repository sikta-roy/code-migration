#include <stddef.h>
#include <limits.h>

int max_diff(const int *l, size_t n) {
    if (n == 0) {
        return 0;
    }

    int max_val = INT_MIN;
    int min_val = INT_MAX;

    for (size_t i = 0; i < n; ++i) {
        if (l[i] > max_val) {
            max_val = l[i];
        }
        if (l[i] < min_val) {
            min_val = l[i];
        }
    }

    return max_val - min_val;
}