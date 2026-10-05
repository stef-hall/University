#include <stdio.h>
#include <stdint.h>

int main(void) {

    union {
        int64_t number;
        unsigned char byte;
        
    } test;

    test.number = 1;

    if (test.byte == 1) {
        printf("Little Endian");
    } else {
        printf("Big Endian");
    }

    return 0;
}