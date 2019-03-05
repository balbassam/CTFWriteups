#include <string.h>
#include <stdio.h>
#include <stdlib.h>

char *enc(const char *input)
{
    // Extracted from binary
    char END;
    int i;
    int STRLEN;
    char *output;

    output = malloc(0x40);
    STRLEN = strlen(input);
    END = 'H';

    for (i = 0; i < STRLEN; ++i)
    {
        output[i] = ((input[i] + 12) * END + 17) % 70 + '0';
        END = output[i];
    }

    return output;
}


int main()
{
    char* SOLUTION = "[OIonU2_<__nK<Ks"; // Encryption output before strcmp

    char* input = calloc(0x40, sizeof(char));
    char* temp;

    // Brute force char by char to get a solution that maps the expected output
    for (int i = 0; i < strlen(SOLUTION); ++i)
    {
        printf("Trying char %d\n", i);
        for (int j = '0'; j <= '~'; ++j)
        {
            input[i] = j;
            temp = enc(input);

            // Increment when a matching character is found
            if(SOLUTION[i] == temp[i]){
                printf("Solution so far is {%s} with temp being {%s}\n",
                        input, temp);
                break;
            }
            free(temp);
        }
    }
}
