#include <stdio.h>

int main(void)
{
   char password = "__stack_check";
   char user_input[100];
   
   printf("Please enter key: ");
   scanf("%s", user_input);
   if (strcmp(user_input, password) == 0)
       printf("Good job.\n");
   else
       printf("Nope.\n");
   return 0;
}
