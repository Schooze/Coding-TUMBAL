from datetime import datetime

# Input tanggal  data mentah
waktu_pinjam_raw = input("Masukkan tanggal buku dipinjam (YYYY-MM-DD): ")
waktu_kembali_raw = input("Masukkan tanggal buku kembali (YYYY-MM-DD): ")

# proses tanggal data mentah
waktu_pinjam_fix = datetime.strptime(waktu_pinjam_raw, "%Y-%m-%d")
waktu_kembali_fix = datetime.strptime(waktu_kembali_raw, "%Y-%m-%d")

# Menghitung selisih antara kedua tanggal
jarak_hari = abs((waktu_kembali_fix - waktu_pinjam_fix).days)

# Memastikan denda awal atau untuk 1 hari
pembayaran = 5000;

# jika lebih dari 1 hari
if (jarak_hari > 1) :

    # Jika lebih dari 5 hari denda 5000 per hari
    if (jarak_hari > 5):
        pembayaran += (5000 * (jarak_hari-1))
   
    # Jika masih 2 - 5 hari denda 3000 per hari
    else :
        pembayaran += (3000 * (jarak_hari-1))

# data anggota premium dan jenis buku
anggota_premium = input("Apakah kamu anggota Premium (Ya/Tidak): ").lower()
jenis_buku = input("Meminjam buku Edukasi(Ya/Tidak): ").lower()



# jika anggota premium
if (anggota_premium == "ya"):
    denda = pembayaran * 0.25
    pembayaran -= denda

# Jika jenis buku edukasi
if (jenis_buku == "ya"):
    denda = pembayaran * 0.1
    pembayaran -= denda

# menghitung denda akhir yang akan di kurangi dengan pembayaran yang seharusnya


# Output harga yang di bayarkan
print("Denda yang di bayarkan",   pembayaran)