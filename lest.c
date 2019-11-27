#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h> 
#include <dirent.h>

void erreur()
{
    fprintf(stderr,"Erreur : %s\n",strerror(errno));
    exit(EXIT_FAILURE);    
}

int main(int argc,char *argv[],char *arge[])
{
DIR *repertoire;
struct dirent *lecture;
int    boucle;

    repertoire=opendir(".");
    if (repertoire==NULL) erreur();
    while ((lecture=readdir(repertoire)))
    {
        if (lecture==NULL) erreur();
        if (lecture->d_name[0]!='.')
        {
            if (argc>1)
            {
                for (boucle=1;boucle<argc;++boucle)
                {
                    if (strcmp(argv[boucle],lecture->d_name)==0)
                    {
                        printf("%s\n",lecture->d_name);
                    }
                }
            }
            else
            {
                printf("%s\n",lecture->d_name);
            }
        }
    }
    closedir(repertoire);
    return EXIT_SUCCESS;
} 
