#include <stdio.h>
#include <stdlib.h>

int safe_divide(double a, double b, double *out) {
    if (b == 0) {
        return -1;  // Error: division by zero
    }
    *out = a / b;
    return 0;  // Success
}