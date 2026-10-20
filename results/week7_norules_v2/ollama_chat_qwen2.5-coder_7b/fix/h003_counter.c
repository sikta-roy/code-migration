#include <stdlib.h>

typedef struct {
    int value;
} Counter;

void counter_init(Counter *c) {
    c->value = 0;
}

void counter_add(Counter *c, int n) {
    c->value += n;
}

void counter_reset(Counter *c) {
    c->value = 0;
}

int counter_get(const Counter *c) {
    return c->value;
}