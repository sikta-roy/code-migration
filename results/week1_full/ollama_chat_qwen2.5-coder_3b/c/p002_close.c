#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>

bool has_close_elements(const double *numbers, size_t n, double threshold) {
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            if (i != j && fabs(numbers[i] - numbers[j]) < threshold) {
                return true;
            }
        }
    }
    return false;
}