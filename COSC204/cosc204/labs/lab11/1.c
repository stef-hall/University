#include <stdio.h>
#include "queue.h"

int main(void) {
    queue *A = queue_new();
    queue_enqueue(A, 1);
    queue *B = queue_deep_copy(A);

    queue_enqueue(A,2);
    queue_enqueue(B,3);

    long long a = (long long) queue_dequeue(A);
    long long b = (long long) queue_dequeue(B);
    printf("Should be matching: %lld | %lld\n", a, b);

    a = (long long) queue_dequeue(A);
    b = (long long) queue_dequeue(B);
    printf("Should be different: %lld | %lld\n", a, b);

}