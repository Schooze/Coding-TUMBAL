z = [[6, 8],
     [14, 8],
     [1,2]]

hasil = [[0,0,0],
         [0,0,0]]

for i in range(len(hasil)):
    for j in range(len(hasil[0])):
        hasil[i][j] = z[j][i]

print("Tugas 1")
print(z)
print(hasil)

x = [[8, 9, 3,],
     [4, 5, 6,], 
     [7, 8, 9]]

y = [[5, 8, 1, 2], 
     [6, 7, 3, 8], 
     [4, 5, 9, 1]]

hasil = [[0,0,0,0], 
         [0,0,0,0],
         [0,0,0,0]]

for i in range(len(hasil)):
    for j in range(len(hasil[0])):
        for k in range(3):
            hasil[i][j] += x[i][k] * y[k][j]
print(hasil)

# # Program untuk mengisi data gedung A dan B pada hari ke 1-7

# def print_data(data):
#     print("\nData Gedung A dan B selama 7 hari:")
#     for i in range(7):
#         print(f"Hari {i+1}: Gedung A = {data['Gedung A'][i]}, Gedung B = {data['Gedung B'][i]}")

# def main():
#     # Inisialisasi array untuk menyimpan data gedung A dan B selama 7 hari
#     data = {
#         "Gedung A": [0] * 7,  # Array dengan 7 elemen default 0
#         "Gedung B": [0] * 7
#     }
    
#     # Mengisi data untuk masing-masing gedung
#     for i in range(7):
#         data["Gedung A"][i] = int(input(f"Masukkan data untuk Gedung A pada hari ke-{i+1}: "))
#         data["Gedung B"][i] = int(input(f"Masukkan data untuk Gedung B pada hari ke-{i+1}: "))
    
#     # Menampilkan hasil
#     print_data(data)
    
# main()  ``