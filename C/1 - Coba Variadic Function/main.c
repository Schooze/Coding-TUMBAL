#include <stdio.h>
#include <stdarg.h>

void VariadicFunc_Exam(int val_1, ...){
    va_list args;
    va_start(args, val_1);
    int re;
    for (int loop = 0; loop < val_1; loop++){
        printf("%d ", va_arg(args, int));
        // printf("%d ", loop);

    }
    va_end(args);
    // return re;
}

int main()
{
    // while (1)
    // {
    VariadicFunc_Exam(3, 3, 4, 5);
    // }
    
    return 0;
}

// #include <stdio.h>
// #include <stdarg.h>

// // Variadic function to print given arguments
// void print(int n, ...) {
//     va_list args;
//     va_start(args, n);  
//     for (int i = 0; i < n; i++) 
//         printf("%d ", va_arg(args, int));
//     printf("\n");
//     va_end(args);
// }


// int main() {
  
//       // Calling function sum() with different number
//       // of arguments
//     print(3, 1, 2, 3);
//     print(5, 1, 2, 3, 4, 5);
  
//     return 0;
// }