#include <stdlib.h>

typedef struct {
    int i;
    int n;
} SquareGen;

void squares_init(SquareGen *g, int n) {
    g->i = 0;
    g->n = n;
}

bool squares_next(SquareGen *g, int *out) {
    if (g->i >= g->n) {
        return false;
    }
    *out = g->i * g->i;
    g->i++;
    return true;
}