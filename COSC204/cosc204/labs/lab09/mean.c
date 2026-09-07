#include <stdio.h>
int main(void)
{   
    int x;
    int tot = 0;
    for (int i=0;i<10;i++){
        scanf("%d", &x);
        tot += x;
    }
    printf("Mean: %d", tot/10);
    return 0;
}