#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int compare(const void *a, const void *b) {
    return strcmp((char *)a, (char *)b);
}

int main() {
    int length = 3;
    char words[length][100];

    for (int i = 0; i < length; i++) {
        scanf("%99s", words[i]);
    }

    qsort(words, length, 100, compare);

    char input[100];

    while (scanf("%99s", input) == 1) {

        char *result = bsearch(input, words, length, 100, compare);

        if (result != NULL) {
            printf("Y\n");
        } else {
            printf("N\n");
        }
    }

    return 0;
}