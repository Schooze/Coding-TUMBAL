
nilai_input = int(input("Masukan mau berapa : "))

# ditambah 2 karena 0 dan 1
for i in range(nilai_input + 2):

    # print menengahnya
    for h in range((nilai_input + 2) - i):
        print(" ", end="")

    # print 1 - 9
    for j in range((i * 2) - 1):

        if i > 10:
            break

        if (j % 2) != 0:
            print(i-1, end='')
        else:
            print(" ", end='')
    
    # print 10 ke atas
    if i > 10:
        for j in range(i-1):
            print(i-1, end='')

    # untuk enter
    print()

