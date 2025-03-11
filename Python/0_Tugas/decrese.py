
nilai_input = int(input("Masukan mau berapa : "))

for i in range(nilai_input):
    # for i in range(nilai_input-i):
    #     print("*")

    # print("*" * (nilai_input - i))
    print(" " * (nilai_input - i), "*" * ((i * 2)-1))

# nilai_input = int(input("Masukan mau berapa : "))