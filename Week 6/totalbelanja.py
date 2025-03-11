# Program menghitung total belanja dengan beberapa kompleksitas algoritma berbeda
import time
import random

# Fungsi dengan kompleksitas O(1) - Konstan
def hitung_total_sederhana(daftar_harga):
    """
    Menghitung total belanja dengan menjumlahkan semua harga.
    Kompleksitas O(1) karena Python sum() diimplementasikan dalam C
    dan performanya mendekati konstan untuk kasus umum.
    """
    return sum(daftar_harga)

# Fungsi dengan kompleksitas O(n) - Linear
def hitung_total_dengan_diskon(daftar_harga, diskon_persen):
    """
    Menghitung total belanja dengan menerapkan diskon pada setiap item.
    Kompleksitas O(n) karena kita melakukan operasi pada setiap item.
    """
    faktor_diskon = 1 - diskon_persen/100
    # Menggunakan list comprehension untuk meningkatkan kecepatan
    return sum(harga * faktor_diskon for harga in daftar_harga)

# Fungsi dengan kompleksitas O(n log n) - Lebih baik dari O(n²)
def hitung_total_dengan_promosi_bundling_optimized(daftar_harga, daftar_nama_produk):
    """
    Menghitung total belanja dengan mencari pasangan bundling yang memberikan diskon.
    Kompleksitas diperbaiki dari O(n²) menjadi mendekati O(n log n) dengan menggunakan
    struktur data dictionary untuk mencari pasangan yang cocok.
    """
    total = sum(daftar_harga)
    diskon_bundling = 0
    
    # Membuat dictionary untuk mencatat indeks produk berdasarkan jenisnya
    kategori_produk = {"shampoo": [], "conditioner": []}
    
    # Mengisi dictionary dengan indeks produk
    for i, nama in enumerate(daftar_nama_produk):
        if "shampoo" in nama:
            kategori_produk["shampoo"].append((i, daftar_harga[i]))
        elif "conditioner" in nama:
            kategori_produk["conditioner"].append((i, daftar_harga[i]))
    
    # Menghitung diskon bundling
    if kategori_produk["shampoo"] and kategori_produk["conditioner"]:
        # Urutkan berdasarkan harga untuk mencari pasangan optimal
        shampoos = sorted(kategori_produk["shampoo"], key=lambda x: x[1])
        conditioners = sorted(kategori_produk["conditioner"], key=lambda x: x[1])
        
        # Pasangkan produk dengan harga terendah untuk memaksimalkan jumlah bundling
        min_pairs = min(len(shampoos), len(conditioners))
        for i in range(min_pairs):
            harga_min = min(shampoos[i][1], conditioners[i][1])
            diskon_bundling += harga_min * 0.2  # Diskon 20% dari harga terendah
    
    return total - diskon_bundling

# Fungsi untuk mengukur waktu eksekusi
def ukur_waktu(fungsi, *args):
    waktu_mulai = time.time()
    hasil = fungsi(*args)
    waktu_selesai = time.time()
    return hasil, (waktu_selesai - waktu_mulai) * 1000  # Konversi ke milidetik

# Fungsi untuk membuat data uji dengan ukuran berbeda
def buat_data_uji(ukuran):
    nama_produk_dasar = ["beras", "telur", "minyak", "sabun", "pasta gigi", "shampoo", "conditioner", 
                     "gula", "susu", "kopi", "teh", "roti", "keju", "sosis", "buah", "sayur"]
    
    # Memastikan ada lebih banyak variasi produk shampoo dan conditioner untuk uji bundling
    produk_tambahan = []
    for i in range(min(ukuran // 10, 10)):  # Menambah beberapa variasi
        produk_tambahan.extend([f"shampoo-{i}", f"conditioner-{i}"])
    
    nama_produk_dasar.extend(produk_tambahan)
    
    daftar_nama_produk = []
    daftar_harga = []
    
    for i in range(ukuran):
        if i < len(nama_produk_dasar):
            nama = nama_produk_dasar[i]
        else:
            # Menambahkan beberapa produk shampoo dan conditioner secara acak
            if random.random() < 0.1:
                nama = f"shampoo-{random.randint(1, 10)}"
            elif random.random() < 0.1:
                nama = f"conditioner-{random.randint(1, 10)}"
            else:
                nama = f"produk-{i}"
        
        daftar_nama_produk.append(nama)
        daftar_harga.append(random.randint(5000, 100000))
    
    return daftar_nama_produk, daftar_harga

# Contoh penggunaan
if __name__ == "__main__":
    # Data belanja kecil untuk demonstrasi
    produk = ["beras", "telur", "minyak goreng", "shampoo", "conditioner", "gula"]
    harga = [65000, 28000, 24000, 35000, 33000, 15000]
    
    print("Daftar Belanja:")
    for i in range(len(produk)):
        print(f"{produk[i]}: Rp{harga[i]}")
    
    # Menghitung dengan berbagai metode
    print("\nHasil Perhitungan untuk 6 item:")
    hasil_o1, waktu_o1 = ukur_waktu(hitung_total_sederhana, harga)
    print(f"Total belanja (O(1)): Rp{hasil_o1}, Waktu: {waktu_o1:.6f} ms")
    
    hasil_on, waktu_on = ukur_waktu(hitung_total_dengan_diskon, harga, 10)
    print(f"Total belanja dengan diskon 10% (O(n)): Rp{hasil_on}, Waktu: {waktu_on:.6f} ms")
    
    hasil_on2, waktu_on2 = ukur_waktu(hitung_total_dengan_promosi_bundling_optimized, harga, produk)
    print(f"Total belanja dengan promosi bundling (O(n log n)): Rp{hasil_on2}, Waktu: {waktu_on2:.6f} ms")
    
    # Uji performa dengan ukuran data yang berbeda
    ukuran_data = [10, 100, 1000, 10000]
    
    print("\nPerbandingan Waktu Eksekusi:")
    print("| Ukuran Data | O(1) (ms) | O(n) (ms) | O(n log n) (ms) |")
    print("|-------------|-----------|-----------|-----------------|")
    
    for ukuran in ukuran_data:
        nama_produk_test, harga_test = buat_data_uji(ukuran)
        
        _, waktu_o1 = ukur_waktu(hitung_total_sederhana, harga_test)
        _, waktu_on = ukur_waktu(hitung_total_dengan_diskon, harga_test, 10)
        _, waktu_on_log_n = ukur_waktu(hitung_total_dengan_promosi_bundling_optimized, harga_test, nama_produk_test)
        
        print(f"| {ukuran:11d} | {waktu_o1:9.6f} | {waktu_on:9.6f} | {waktu_on_log_n:15.6f} |")

