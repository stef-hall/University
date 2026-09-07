#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{   

    printf("size of: char[%d]  int[%d]  float[%d]\n", (int) sizeof(char), (int) sizeof(int), (int) sizeof(float));


    char *words[100];

    for (int i=0;i<100;i++) {
        words[i] = malloc(1);
        words[i][0] = '\0';
    }


    for (int i=0;i<100;i++) {
        char str[100];                  // Initalise temp str
        if (scanf("%79s", str) != 1){
            break;
        }
        free(words[i]);
        words[i] = malloc((strlen(str) + 1) * sizeof(char)); //Allocate new temp space + Terminator
        strcpy(words[i], str);              //Copy str into words[i]
    }

    int temp = 0;
    double average = 0;
    for (int i=0;i<100;i++) {
        int length = strlen(words[i]);
        if (length != 0) {
            temp++;
            average += length;
        }
    }

    if (temp > 0) {
        average = average / temp;
        printf("Average word length: %.2f\n", average);
    }

    for (int i=0;i<100;i++) {
        if (strlen(words[i]) > average) {
          printf("%s\n", words[i]);  
        }
    }

    for (int i = 0; i < 100; i++) {
        free(words[i]);
    }


    return 0;

}
