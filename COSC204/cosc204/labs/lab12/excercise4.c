#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int compare (const void *a, const void *b) {
    return strcmp((char *)a, (char *)b);
}

int main () {
    int length = 3;
    char words[length][100];

    for (int i=0;i<length;i++){
        scanf(" %99s", words[i]);
    }

    qsort(words, length, 100, compare);

    for (int i=0;i<length;i++) {
        printf("Word: %s\n", words[i]);
    }

    char input[100];
    while (1) {
        scanf("%99s",input);
        
        char *result = bsearch(input, words, length, 100, compare);
        if (result != NULL) {
            printf("Yea its there\n");
        }

    }
    
    return 0;
}