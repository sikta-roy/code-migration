#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

static int cmp(const void *a, const void *b) 
{
    return *(int*)a - *(int*)b;
}

int *sort_asc(const int *l, size_t n, size_t *out_len) 
{
    int *result = malloc(n * sizeof(int));
    memcpy(result, l, n * sizeof(int));
    qsort(result, n, sizeof(int), cmp);
    *out_len = n;
    return result;
}