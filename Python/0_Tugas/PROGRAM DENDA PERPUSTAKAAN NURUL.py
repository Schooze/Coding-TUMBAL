from datetime import datetime

# Input tanggal peminjaman dan pengembalian
tanggal_pinjam = input("Masukkan tanggal peminjaman (dd-mm-yyyy): ")
tanggal_kembali = input("Masukkan tanggal pengembalian (dd-mm-yyyy): ")

# Konversi string menjadi objek datetime
tgl_pinjam = datetime.strptime(tanggal_pinjam, "%d-%m-%Y")
tgl_kembali = datetime.strptime(tanggal_kembali, "%d-%m-%Y")

# Menghitung selisih hari
HARI = (tgl_kembali - tgl_pinjam).days

# Input jenis anggota dan jenis buku
ANGGOTAPREMIUM = input("Apakah anggota premium? (yes/no): ").lower() == "yes"
BUKUEDUKASI = input("Apakah buku edukasi? (yes/no): ").lower() == "yes"

# Perhitungan denda awal
if HARI <= 0:
    DENDATOTAL = 0  # Tidak ada denda jika tidak terlambat
elif HARI == 1:
    DENDATOTAL = 5000
elif HARI >= 6:
    DENDATOTAL = 17000 + (HARI - 5) * 5000
else:
    DENDATOTAL = 5000 + (HARI - 1) * 3000

# Diskon untuk anggota premium
if ANGGOTAPREMIUM:
    DENDATOTAL *= 0.75  # Diskon 25%

# Diskon untuk buku edukasi
if BUKUEDUKASI:
    DENDATOTAL *= 0.90  # Diskon 10%

# Output hasil akhir
print(f"Total denda yang harus dibayar: Rp {DENDATOTAL: }")