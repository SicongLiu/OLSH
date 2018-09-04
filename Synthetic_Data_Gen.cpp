
// ***************************************************************************
// ** Datengenerierung **
// source: https://github.com/sofiabravo103/builder
// ***************************************************************************

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>

// #ifdef CYGWIN
#define MAXINT 2147483647
// #else
// #define MAXINT 32767
// #endif

#define sqr(a) ((a)*(a))


int Statistics_Count;
double* Statistics_SumX;
double* Statistics_SumXsquared;
double* Statistics_SumProduct;


void InitStatistics(int Dimensions)
// ==============
// initialisiert Zählvariablen der Statistik
{
    Statistics_SumX = new double[Dimensions];
    Statistics_SumXsquared = new double[Dimensions];
    Statistics_SumProduct = new double[Dimensions*Dimensions];
    
    Statistics_Count = 0;
    for (int d=0; d<Dimensions; d++)
    {
        Statistics_SumX[d]=0.0;
        Statistics_SumXsquared[d]=0.0;
        for (int dd=0; dd<Dimensions; dd++)
            Statistics_SumProduct[d*Dimensions+dd] = 0.0;
    }
}


void EnterStatistics(int Dimensions,double* x)
// ===============
// registiriert den Vektor "x" für die Statistik
{
    Statistics_Count++;
    for (int d=0; d<Dimensions; d++) {
        Statistics_SumX[d] += x[d];
        Statistics_SumXsquared[d] += x[d]*x[d];
        for (int dd=0; dd<Dimensions; dd++) Statistics_SumProduct[d*Dimensions+dd] += x[d]*x[dd];
    }
}


void OutputStatistics(int Dimensions)
// ================
// gibt die Statistik aus
{
    for (int d=0; d<Dimensions; d++) {
        double E = Statistics_SumX[d] / Statistics_Count;
        double V = Statistics_SumXsquared[d]/Statistics_Count - E*E;
        double s = sqrt(V);
        printf("E[X%d]=%5.2f Var[X%d]=%5.2f s[X%d]=%5.2f\n",d+1,E,d+1,V,d+1,s);
    }
    printf("\nKorrelationsmatrix:\n");
    for (int d=0; d<Dimensions; d++) {
        for (int dd=0; dd<Dimensions; dd++) {
            double Kov = (Statistics_SumProduct[d*Dimensions+dd]/Statistics_Count) -
            (Statistics_SumX[d]/Statistics_Count) * (Statistics_SumX[dd]/Statistics_Count);
            double Cor = Kov /
            sqrt(Statistics_SumXsquared[d]/Statistics_Count - sqr(Statistics_SumX[d] / Statistics_Count)) /
            sqrt(Statistics_SumXsquared[dd]/Statistics_Count - sqr(Statistics_SumX[dd] / Statistics_Count));
            printf(" %5.2f",Cor);
        }
        printf("\n");
    }
    printf("\n");
}


double RandomEqual(double min,double max)
// ===========
// liefert eine im Intervall [min,max[ gleichverteilte Zufallszahl
{
    double x = (double)rand()/MAXINT;
    return x*(max-min)+min;
}


double RandomPeak(double min,double max,int dim)
// ==========
// liefert eine Zufallsvariable im Intervall [min,max[
// als Summe von "dim" gleichverteilten Zufallszahlen
{
    double sum = 0.0;
    for (int d=0; d<dim; d++) sum += RandomEqual(0,1);
    sum /= dim;
    return sum*(max-min)+min;
}


double RandomNormal(double med,double var)
// ============
// liefert eine normalverteilte Zufallsvariable mit Erwartungswert med
// im Intervall ]med-var,med+var[
{
    return RandomPeak(med-var,med+var,12);
}


void GenerateDataEqually(FILE* f,int Count,int Dimensions)
// ===================
// generiert in der Datei "f" "Count" gleichverteilte Datensätze
{
    InitStatistics(Dimensions);
    for (int i=0; i<Count; i++)
    {
        double x[Dimensions];
        for (int d=0; d<Dimensions; d++)
        {
            x[d] = RandomEqual(0,1);
            fprintf(f,"%8.6f ",x[d]);
        }
        EnterStatistics(Dimensions,x);
        fprintf(f,"\n");
    }
    //OutputStatistics(Dimensions);
}


void GenerateDataCorrelated(FILE* f,int Count,int Dimensions)
// ======================
// generiert in der Datei "f" "Count" korrelierte Datensätze
{
    InitStatistics(Dimensions);
    double x[Dimensions];
    for (int i=0; i<Count; i++)
    {
    again:
        double v = RandomPeak(0,1,Dimensions);
        for (int d=0; d<Dimensions; d++)
        {
            x[d] = v;
        }
        double l = v<=0.5 ? v:1.0-v;
        for (int d=0; d<Dimensions; d++)
        {
            double h = RandomNormal(0,l);
            x[d] += h;
            x[(d+1)%Dimensions] -= h;
        }
        for (int d=0; d<Dimensions; d++)
            if (x[d]<0 || x[d]>=1)
                goto again;
        
        for (int d=0; d<Dimensions; d++)
            fprintf(f,"%8.6f ",x[d]);
        
        EnterStatistics(Dimensions,x);
        
        fprintf(f,"\n");
    }
    OutputStatistics(Dimensions);
}


void GenerateDataAnticorrelated(FILE* f,int Count,int Dimensions)
// ==========================
// generiert in der Datei "f" "Count" antikorrelierte Datensätze
{
    InitStatistics(Dimensions);
    double x[Dimensions];
    for (int i=0; i<Count; i++) {
    again:
        double v = RandomNormal(0.5,0.25);
        for (int d=0; d<Dimensions; d++)
            x[d] = v;
        double l = v<=0.5 ? v:1.0-v;
        for (int d=0; d<Dimensions; d++) {
            double h = RandomEqual(-l,l);
            x[d] += h;
            x[(d+1)%Dimensions] -= h;
        }
        for (int d=0; d<Dimensions; d++) if (x[d]<0 || x[d]>=1) goto again;
        for (int d=0; d<Dimensions; d++) fprintf(f,"%8.6f ",x[d]);
        EnterStatistics(Dimensions,x);
        fprintf(f,"\n");
    }
    OutputStatistics(Dimensions);
}

/*
void GenerateData(int Dimensions,char Distribution,int Count,char* FileName)
// ============
// generierte eine Datei mit zufälligen Daten
{
    if (Count <= 0) {
        printf("Ungültige Anzahl von Punkten.\n");
        return;
    }
    if (Dimensions < 2) {
        printf("Ungültige Anzahl von Dimensionen.\n");
        return;
    }
    switch (Distribution) {
        case 'E':
        case 'e': Distribution = 'E'; break;
        case 'C':
        case 'c': Distribution = 'C'; break;
        case 'A':
        case 'a': Distribution = 'A'; break;
        default: printf("Ungültige Verteilung.\n"); return;
    }
    
    FILE* f = fopen(FileName,"wt");
    if (f == NULL) {
        printf("Kann Datei \"%s\" nicht anlegen.\n",FileName);
        return;
    }
    fprintf(f,"%d %d\n",Count,Dimensions);
    switch (Distribution) {
        case 'E': GenerateDataEqually(f,Count,Dimensions); break;
        case 'C': GenerateDataCorrelated(f,Count,Dimensions); break;
        case 'A': GenerateDataAnticorrelated(f,Count,Dimensions); break;
    }
    fclose(f);
    printf("%d Punkte generiert, Datei \"%s\".\n",Count,FileName);
}
*/

int main(int argc, char** argv)
// ====
// main program
{
    char* FileName1 = "correlated.txt";
    char* FileName2 = "anti_correlated.txt";
    char* FileName3 = "random.txt";
    FILE* f1 = fopen(FileName1,"wt");
    FILE* f2 = fopen(FileName2,"wt");
    FILE* f3 = fopen(FileName3,"wt");
    int dimension = 2;
    int count = 1000;
    
    fprintf(f1,"%d", dimension);
    fprintf(f1,"\n");
    fprintf(f1,"%d", count);
    fprintf(f1,"\n");
    GenerateDataCorrelated(f1, count, dimension);
    
    fprintf(f2,"%d", dimension);
    fprintf(f2,"\n");
    fprintf(f2,"%d", count);
    fprintf(f2,"\n");
    GenerateDataAnticorrelated(f2, count, dimension);
    
    fprintf(f3,"%d", dimension);
    fprintf(f3,"\n");
    fprintf(f3,"%d", count);
    fprintf(f3,"\n");
    GenerateDataEqually(f3, count, dimension);
    
    return 0;
}










