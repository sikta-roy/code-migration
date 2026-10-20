#include <stdlib.h>

int gcd(int a, int b) {
    while (b) {
        int temp = a;
        a = b;
        b = temp % b;
    }
    return abs(a);
}