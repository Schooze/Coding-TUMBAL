#include "Coba_Akses_File_Lain.h"
#include <stdio.h>

// extern int akses_lain;

// extern void ini_fungsi();

int main (){

    akses_lain++;
    akses_lain++;
    akses_lain++;
    akses_lain++;

    printf("%d", akses_lain);

    ini_fungsi();

    printf("%d", akses_lain);
}