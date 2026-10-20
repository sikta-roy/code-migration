#include <stddef.h>
#include <stdbool.h>

bool find_index(const int *l, size_t n, int target, size_t *out_index) {
    for (size_t i = 0; i < n; ++i) {
        if (l[i] == target) {
            *out_index = i;
            return true;
        }
    }
    return false;
}