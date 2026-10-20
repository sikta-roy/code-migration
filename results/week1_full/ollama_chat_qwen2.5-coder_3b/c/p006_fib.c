#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>

long long fib(int n) {
    long long a = 0, b = 1;
    for (int _ = 0; _ < n; _++) {
        long long temp = b;
        b = a + b;
        a = temp;
    }
    return a;
}