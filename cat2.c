#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

int main(int argc,char *argv[],char *arge[])
{
int boucle;
FILE *fichier;
char buffer[32768];
int     lecture;

    if (argc<2) exit (0);
    for (boucle=1;boucle<argc;++boucle)
    {
        fichier=fopen(argv[boucle],"r");
        if (fichier!=NULL)
        {
            lecture=-1;
            while (lecture!=0)
            {
                lecture=fread(buffer,1,32768,fichier);
                if (lecture!=0) fwrite(buffer,1,lecture,stdout);
            }
            if (feof(fichier)==0) fprintf(stderr,"cat: %s: %s\n",argv[boucle],strerror(errno));
            fclose(fichier);
        }
        else
        {
            fprintf(stderr,"cat: %s: %s\n",argv[boucle],strerror(errno));
        }
    }
    return 0;
}
