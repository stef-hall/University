#include <stdio.h>
#include <stdint.h>

void print_binary(int value, int bits) {
    for (int i=bits-1; i >= 0; i--) {
        printf("%i", (value >> i) & 1);
    }
    printf(" ");
}

int main(void){
    struct ieee
    {
    unsigned int mantissa:23;
    unsigned int exponent:8;
    unsigned int sign:1;
    };

    union {
        float number;
        struct ieee disect;
    } test;


    printf("Number:");
    scanf("%f", &test.number);

    printf("Sign: %i\n", test.disect.sign);
    printf("Exponent: %i\n", test.disect.exponent);
    printf("Mantissa: %i\n", test.disect.mantissa);


    print_binary(test.disect.sign, 1);
    print_binary(test.disect.exponent, 8);
    print_binary(test.disect.mantissa, 23);
    

}