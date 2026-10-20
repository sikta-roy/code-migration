#include <stddef.h>

long long fib(int n) {
    long long a = 0, b = 1;
    for (size_t i = 0; i < n; i++) {
        long long temp = a;
        a = b;
        b = temp + b;
    }
    return a;
}