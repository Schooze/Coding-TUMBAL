#include <iostream>


char var[10] = "Saya apa";

int var_int;

void coba_pointer(void *nilai){
    std::cout << nilai << std::endl;
}

int main(){
    var_int = 10;

    int *var_1 = &var_int; 
    int **var_2 = &var_1; 

    // coba_pointer(var);
    // coba_pointer(var_1);
    // coba_pointer(&var_int);

    std::cout << var_2 << std::endl;
    std::cout << *var_2 << std::endl;
    std::cout << **var_2 << std::endl;



    std::cout << &var_int << std::endl;

    std::cout << &var_1 << std::endl;

    std::cin.get();


}