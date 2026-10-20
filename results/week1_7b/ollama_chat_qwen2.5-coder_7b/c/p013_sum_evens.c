#include <stddef.h>

long long sum_evens(const int *l, size_t n) {
    long long sum = 0;
    for (size_t i = 0; i < n; i++) {
        if (l[i] % 2 == 0) {
            sum += l[i];
        }
    }
    return sum;
}