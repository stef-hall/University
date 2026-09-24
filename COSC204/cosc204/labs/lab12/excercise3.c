#include <stdio.h>
#include <stdlib.h>
int compare (const void *a, const void *b) {
    int first = *(int*) a;
    int second = *(int *) b;
    if (first < second) return -1;
    else if (first == second) return 0;
    else return 1;
}

int main () {
    int arr[] = {10, 5, 15, 12, 90, 80};
    qsort(arr, 6, sizeof(int), compare);
    for (int i = 0; i < 6; i++) {
        printf ("%d ", arr[i]);
    }
    
    return 0;
}