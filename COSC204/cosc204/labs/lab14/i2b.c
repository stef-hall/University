#include <stdio.h>

void PrintBinary(int num, int length){
    for (int i=0;i<length;i++) {
        int result = (num >> (length-i)-1) & 1;
        printf("%i", result);
    }
}

int main(void) {
    int number = 13;
    PrintBinary(number, 5);

    return 0;
}