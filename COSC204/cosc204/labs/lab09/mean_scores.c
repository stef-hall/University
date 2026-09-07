#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b)
{
    double da = *(const double *)a;
    double db = *(const double *)b;

    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

int main(void)
{   
    double scores[4];
    for (int i=0;i<4;i++){
        double indvScores[5];
        scanf("%lf %lf %lf %lf %lf", &indvScores[0], &indvScores[1], &indvScores[2],&indvScores[3],&indvScores[4]);
        qsort(indvScores, 4, sizeof(double), compare);

        double temp = 0;

        for (int x=1;x<4;x++){
            temp += indvScores[x];
        }
        scores[i] = (temp/3);

    }

    for (int i = 0; i < 4; i++) {
        printf("%.5f ", scores[i]);
    }

    return 0;
}