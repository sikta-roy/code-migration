#include <stdlib.h>
#include <math.h>

typedef struct {
    double x;
    double y;
} Point;

double point_distance(Point a, Point b) {
    return sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2));
}