#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include <math.h>

int gcd(int a, int b) {
    while (b) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return abs(a);
}