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
        qsort(indvScores, 5, sizeof(double), compare);

        double temp = 0;

        for (int x=1;x<4;x++){
            temp += indvScores[x];
        }

        scores[i] = (temp/3);

        printf("Competitor %d scores %lf from: %lf %lf %lf %lf %lf\n", i+1, (temp/3), indvScores[0], indvScores[1], indvScores[2], indvScores[3], indvScores[4]);

    }


    double ranked_scores[4];
    for (int i=0;i<4;i++){
        ranked_scores[i] = scores[i];
    }

    qsort(ranked_scores, 4, sizeof(double), compare);
    
    for (int i = 0; i < 4; i++) {
        if (scores[i] == ranked_scores[3]) {
            printf("\nCompetitor %d wins with a Average Score of %.5f\n", i+1, scores[i]);
        }
    }


    return 0;

}

//4.4 4.6 6.0 1.0 9.0
//0.0 0.0 0.0 0.0 0.0