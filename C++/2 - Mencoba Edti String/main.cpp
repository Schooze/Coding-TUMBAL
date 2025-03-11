#include <iostream>
#include <string>

int main() {
    int num = 42;
    std::string str = std::to_string(num); // Konversi int ke string
    std::cout << "String: " << str << std::endl;

    float value = std::stof("3.14"); // Konversi string ke float
    std::cout << "Float: " << value << std::endl;

    return 0;
}