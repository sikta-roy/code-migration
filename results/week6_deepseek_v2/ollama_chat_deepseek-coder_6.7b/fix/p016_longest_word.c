#include <stdlib.h>
#include <string.h>

char *longest_word(const char *s) 
{
    char *duplicate = strdup(s);
    const char delim[2] = " ";
    char *token;

    if (!duplicate)
        return NULL;

    token = strtok(duplicate, delim);
    if (!token) 
    {
        free(duplicate);
        return NULL;
    }

    char *best = token;
    while ((token = strtok(NULL, delim))) 
    {
        if (strlen(token) > strlen(best)) 
        {
            best = token;
        }
    }

    free(duplicate);
    return best;
}