#include <stdlib.h>

int *flatten_evens(const int *grid, size_t rows, size_t cols, size_t *out_len) {
    size_t count = 0;
    // Count the number of even numbers
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            if (grid[i * cols + j] % 2 == 0) {
                ++count;
            }
        }
    }

    // Allocate memory for the result
    int *result = (int *)malloc(count * sizeof(int));
    if (result == NULL) {
        *out_len = 0;
        return NULL;
    }

    // Fill the result array with even numbers
    size_t index = 0;
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            if (grid[i * cols + j] % 2 == 0) {
                result[index++] = grid[i * cols + j];
            }
        }
    }

    *out_len = count;
    return result;
}