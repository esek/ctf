#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    printf("Enter the secret of this task to continue:\n");
    fflush(stdout);

    char passwordCorrect = 0;
    char buffer[20];

    gets(buffer);

    if (strcmp(buffer, "PASSWORD") == 0)
    {
        passwordCorrect = 1;
        printf("Password is correct! Unlocking...\n");
        fflush(stdout);
    }
    else
    {
        printf("Password is incorrect!");
        fflush(stdout);
    }

    if (passwordCorrect)
    {
        const char *secret = getenv("CTF_SECRET");
        printf(secret, "%s\n");
        fflush(stdout);
    }

    return 0;
}