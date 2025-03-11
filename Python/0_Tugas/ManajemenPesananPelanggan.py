# import datetime

menu = ("bakso", "soto", "mie ayam")
print(menu)

menu_now = []

while True:
    pilihan_menu = input("Makanan yang dipesan : ").lower()

    if pilihan_menu in menu:

        menu_now.append(pilihan_menu)

        print("Menu yang di pilih : ")
        print(menu_now)
        tambah_pesanan = input("Menambah pesanan (ya/tidak) : ").lower()

        if (tambah_pesanan == "tidak"):
            break
    else:
        print("Memesan menu yang salah")

