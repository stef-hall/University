#include <stdio.h>

void fun(int a, char b)
{
printf("Value of a is %d | C is gay: %c\n", a, b);
}

int main()
{
void (*fun_ptr)(int, char) = fun;
fun_ptr(10, 'A');

fun(11, 'B');

return 0;
}