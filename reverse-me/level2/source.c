#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

void no()
{
    puts("Nope.");
    exit(1);
}

void ok()
{
    puts("Good job.");
}


// The way the password works is taking user input, converting it as if groups of 3 characters represent an ascii value.
// After the entire input string has been converted the result should be "delabere".
int main(void)
{
    char     atoi_input[4];
    char     ascii_values[24];
    char     converted_input[9];
    size_t   input_len;
    uint32_t user_input_index;
    int32_t  ascii_str_index;
    int32_t  scanf_ret;
    uint32_t input_len_check;
    bool     still_inside_input;

    printf("Please enter key: ");
    scanf_ret = scanf("%23s",ascii_values);
    if (scanf_ret != 1 || ascii_values[0] != '0' || ascii_values[1] != '0')
        no();

    fflush(stdin);
    input_len = strlen(ascii_values);

    memset(converted_input, 0, 9);
    // Initialize the converted string with 'd' at the start since the first char will be skipped 
    converted_input[0] = 'd';
    
    // The first 2 chars from the user input have to be '0' and '0', so we skip those
    user_input_index = 2;

    // We skip the first char since it is already initialized as 'd'
    ascii_str_index = 1;

    // make sure the atoi input is terminated 
    atoi_input[3] = '\0';
    while( true )
    {
        still_inside_input = false;
        if (strlen(converted_input) < 8)
        {
            still_inside_input = user_input_index < input_len;
        }
        if (!still_inside_input)
            break;

        atoi_input[0] = ascii_values[user_input_index];
        atoi_input[1] = ascii_values[user_input_index + 1];
        atoi_input[2] = ascii_values[user_input_index + 2];

        converted_input[ascii_str_index] = (char)atoi(atoi_input);
        user_input_index += 3;
        ascii_str_index += 1;
    }
    converted_input[ascii_str_index] = '\0';

    // Compare the converted input with the password 'delabere'
    if (strcmp(converted_input, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
