#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>  

int main () {
    FILE *fp,*fp1;
    char pwd[40];
    char * line = NULL;
    size_t len = 0;
        char s[100]; 

    char dest[50];
    ssize_t read;
    bool homeflag = false;
    bool pathflag = false;
    fp1 = popen("pwd", "r");
    while (fgets(pwd, sizeof(pwd), fp1) != NULL) 
        {
            printf("%s", pwd);

        }
    pclose(fp1);

  

    fp = fopen("Profile", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    while ((read = getline(&line, &len, fp)) != -1) {
        printf("%s", line);
        char *ptr5 = strstr(line, "PATH");
        char *ptr4 = strstr(line, "HOME");
        if (ptr5 != NULL) /* Substring found */
            {
                pathflag = true;
            }

        if (ptr4 != NULL) /* Substring found */
            {
                homeflag = true;
                strcpy(dest, line+5);
            }
        
    }
    if( homeflag == false || pathflag == false)
    {
        printf("%s", "path or home not found\n");
    }
    fclose(fp);
      
   chdir(dest); 
   printf("%s\n", getcwd(s, 100)); 

   //char command[50];
   //char pwd[50];
   //strcpy(command, "pwd" );
   //printf(popen(command, "r"));
   return(0);
} 
