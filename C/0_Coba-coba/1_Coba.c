#include <stdio.h>

typedef struct {
    const char *id;  // Menyimpan ID elemen
    struct {
        struct {
            int width;
            int height;
        } sizing;
        struct {
            int y;
        } childAlignment;
        struct {
            int top;
            int right;
            int bottom;
            int left;
        } padding;
    } layout;
} ClayElement;

ClayElement coba;

int main(){

    while (1){

        

    }
}