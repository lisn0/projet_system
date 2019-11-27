#include <unistd.h>
#include <stdio.h>

int main()
{
    char dossier_en_cours[4096];
    getcwd(dossier_en_cours,4096);
    printf("%s\n",dossier_en_cours);
    return 0;
} 
