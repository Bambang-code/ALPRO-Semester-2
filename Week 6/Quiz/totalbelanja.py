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

# Fungsi dengan kompleksitas O(n²) - Kuadratik
def hitung_total_dengan_promosi_bundling_on2(daftar_harga, daftar_nama_produk, pasangan_bundling):
    """
    Menghitung total belanja dengan mencari pasangan bundling yang memberikan diskon.
    Kompleksitas O(n²) karena kita membandingkan setiap produk dengan semua produk lainnya.
    
    Args:
        daftar_harga: List harga produk
        daftar_nama_produk: List nama produk
        pasangan_bundling: List tuple (kata_kunci1, kata_kunci2, diskon_persen)
    """
    total = sum(daftar_harga)
    diskon_bundling = 0
    produk_terbundling = set()  # Mencatat produk yang sudah terbundling
    pasangan_ditemukan = []
    
    # Jika tidak ada pasangan bundling, gunakan default shampoo-conditioner
    if not pasangan_bundling:
        pasangan_bundling = [("shampoo", "conditioner", 20)]
    
    # Bandingkan setiap produk dengan semua produk lainnya - pendekatan O(n²)
    for i in range(len(daftar_nama_produk)):
        if i in produk_terbundling:
            continue  # Produk sudah terbundling, lewati
            
        for j in range(i+1, len(daftar_nama_produk)):
            if j in produk_terbundling:
                continue  # Produk sudah terbundling, lewati
            
            # Periksa semua pasangan bundling
            for kata_kunci1, kata_kunci2, diskon_persen in pasangan_bundling:
                pair_found = False
                # Cek apakah pasangan kata kunci ditemukan
                if kata_kunci1.lower() in daftar_nama_produk[i].lower() and kata_kunci2.lower() in daftar_nama_produk[j].lower():
                    pair_found = True
                elif kata_kunci2.lower() in daftar_nama_produk[i].lower() and kata_kunci1.lower() in daftar_nama_produk[j].lower():
                    pair_found = True
                    
                if pair_found:
                    # Hitung diskon berdasarkan persentase dari harga terendah
                    harga_min = min(daftar_harga[i], daftar_harga[j])
                    diskon = harga_min * (diskon_persen / 100)
                    diskon_bundling += diskon
                    produk_terbundling.add(i)
                    produk_terbundling.add(j)
                    pasangan_ditemukan.append((i, j, kata_kunci1, kata_kunci2, diskon_persen, diskon))
                    break  # Setelah menemukan pasangan, hentikan pencarian untuk produk ini
            
            if i in produk_terbundling:
                break  # Jika sudah terbundling, lanjut ke produk berikutnya
    
    return total - diskon_bundling, pasangan_ditemukan

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

# Fungsi untuk mendapatkan data demo
def get_data_demo():
    produk = ["beras", "telur", "minyak goreng", "shampoo", "conditioner", "gula"]
    harga = [65000, 28000, 24000, 35000, 33000, 15000]
    return produk, harga

# Fungsi untuk mendapatkan data demo ukuran besar dengan bundling yang jelas
def get_data_demo_besar():
    produk = [
        "beras premium", "telur ayam kampung", "minyak goreng", "bawang merah", "bawang putih",
        "gula pasir", "kecap manis", "saus sambal", "shampoo anti ketombe", "conditioner rambut keriting",
        "sabun mandi", "pasta gigi", "sikat gigi", "deterjen", "pelembut pakaian",
        "kopi bubuk", "teh celup", "susu bubuk", "shampoo bayi", "conditioner bayi",
        "roti tawar", "selai cokelat", "selai kacang", "shampoo anti rontok", "conditioner vitamin",
        "mie instan", "biskuit", "keripik kentang"
    ]
    
    harga = [
        65000, 28000, 24000, 15000, 12000,
        15000, 8000, 7500, 35000, 33000,
        7000, 8500, 5000, 18000, 15500,
        25000, 12000, 45000, 38000, 36000,
        14000, 22000, 23000, 42000, 38000,
        3500, 9500, 8500
    ]
    
    return produk, harga

# Fungsi baru untuk input user
def input_daftar_belanja():
    produk = []
    harga = []
    
    print("\n=== PROGRAM MENGHITUNG TOTAL BELANJA ===")
    print("Input daftar belanja Anda (ketik 'selesai' untuk mengakhiri)")
    
    while True:
        nama_produk = input("\nMasukkan nama produk (atau 'selesai' untuk mengakhiri): ")
        if nama_produk.lower() == 'selesai':
            break
        
        try:
            harga_produk = int(input("Masukkan harga produk (Rp): "))
            if harga_produk < 0:
                print("Harga tidak boleh negatif. Coba lagi.")
                continue
        except ValueError:
            print("Input harga tidak valid. Masukkan angka bulat.")
            continue
        
        produk.append(nama_produk)
        harga.append(harga_produk)
        print(f"Produk '{nama_produk}' dengan harga Rp{harga_produk} telah ditambahkan.")
    
    return produk, harga

# Fungsi untuk menginput promosi bundling
def input_promosi_bundling():
    pasangan_bundling = []
    
    print("\n=== INPUT PROMOSI BUNDLING ===")
    print("Masukkan pasangan kata kunci dan persentase diskon (ketik 'selesai' pada kata kunci pertama untuk mengakhiri)")
    
    while True:
        kata_kunci1 = input("\nMasukkan kata kunci produk pertama (atau 'selesai' untuk mengakhiri): ")
        if kata_kunci1.lower() == 'selesai':
            break
        
        kata_kunci2 = input("Masukkan kata kunci produk kedua: ")
        
        try:
            diskon_persen = float(input("Masukkan persentase diskon (%): "))
            if diskon_persen <= 0 or diskon_persen > 100:
                print("Persentase diskon harus di antara 0 dan 100. Coba lagi.")
                continue
        except ValueError:
            print("Input persentase diskon tidak valid. Masukkan angka.")
            continue
        
        pasangan_bundling.append((kata_kunci1, kata_kunci2, diskon_persen))
        print(f"Promosi bundling '{kata_kunci1}' + '{kata_kunci2}' dengan diskon {diskon_persen}% telah ditambahkan.")
    
    return pasangan_bundling

# Fungsi untuk menampilkan menu algoritma
def pilih_algoritma():
    while True:
        print("\n=== PILIH ALGORITMA PERHITUNGAN ===")
        print("1. Hitung total sederhana (O(1))")
        print("2. Hitung dengan diskon (O(n))")
        print("3. Hitung dengan promosi bundling (O(n²))")
        print("4. Bandingkan semua algoritma")
        print("5. Kembali ke menu utama")
        
        try:
            pilihan = int(input("Pilih algoritma (1-5): "))
            if 1 <= pilihan <= 5:
                return pilihan
            else:
                print("Pilihan tidak valid. Masukkan angka 1-5.")
        except ValueError:
            print("Input tidak valid. Masukkan angka 1-5.")

# Fungsi untuk menampilkan menu data demo
def pilih_data_demo():
    while True:
        print("\n=== PILIH DATA DEMO ===")
        print("1. Data demo kecil (6 item)")
        print("2. Data demo besar (28 item dengan beberapa pasangan bundling)")
        print("3. Kembali ke menu utama")
        
        try:
            pilihan = int(input("Pilih data demo (1-3): "))
            if pilihan == 1:
                return get_data_demo()
            elif pilihan == 2:
                return get_data_demo_besar()
            elif pilihan == 3:
                return [], []
            else:
                print("Pilihan tidak valid. Masukkan angka 1-3.")
        except ValueError:
            print("Input tidak valid. Masukkan angka 1-3.")

# Fungsi untuk menampilkan menu utama
def menu_utama():
    produk = []
    harga = []
    pasangan_bundling = []
    
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Input daftar belanja")
        print("2. Gunakan data demo")
        print("3. Input promosi bundling")
        print("4. Lihat daftar belanja")
        print("5. Lihat promosi bundling")
        print("6. Hitung total belanja")
        print("7. Uji performa algoritma")
        print("8. Keluar")
        
        try:
            pilihan = int(input("Pilih menu (1-8): "))
            
            if pilihan == 1:
                produk, harga = input_daftar_belanja()
            
            elif pilihan == 2:
                demo_produk, demo_harga = pilih_data_demo()
                if demo_produk and demo_harga:
                    produk, harga = demo_produk, demo_harga
                    print("\nData demo berhasil dimuat!")
                    print("\nDaftar Belanja Demo:")
                    for i in range(len(produk)):
                        print(f"{i+1}. {produk[i]}: Rp{harga[i]}")
            
            elif pilihan == 3:
                new_pasangan_bundling = input_promosi_bundling()
                if new_pasangan_bundling:
                    pasangan_bundling = new_pasangan_bundling
                    print(f"\nTotal {len(pasangan_bundling)} promosi bundling telah ditambahkan!")
            
            elif pilihan == 4:
                if not produk:
                    print("Daftar belanja kosong. Silakan input daftar belanja atau gunakan data demo terlebih dahulu.")
                    continue
                
                print("\nDaftar Belanja:")
                for i in range(len(produk)):
                    print(f"{i+1}. {produk[i]}: Rp{harga[i]}")
                print(f"\nTotal item: {len(produk)}")
                print(f"Total harga (tanpa diskon/promosi): Rp{sum(harga)}")
            
            elif pilihan == 5:
                if not pasangan_bundling:
                    print("Belum ada promosi bundling. Silakan input promosi bundling terlebih dahulu.")
                    print("Promosi default shampoo + conditioner dengan diskon 20% akan digunakan.")
                    continue
                
                print("\nDaftar Promosi Bundling:")
                for i, (kunci1, kunci2, diskon) in enumerate(pasangan_bundling):
                    print(f"{i+1}. '{kunci1}' + '{kunci2}' = Diskon {diskon}%")
            
            elif pilihan == 6:
                if not produk:
                    print("Daftar belanja kosong. Silakan input daftar belanja atau gunakan data demo terlebih dahulu.")
                    continue
                
                algoritma = pilih_algoritma()
                
                if algoritma == 1:
                    hasil, waktu = ukur_waktu(hitung_total_sederhana, harga)
                    print(f"\nTotal belanja (O(1)): Rp{hasil:.2f}, Waktu: {waktu:.6f} ms")
                
                elif algoritma == 2:
                    try:
                        diskon = float(input("Masukkan persentase diskon (%): "))
                        if diskon < 0 or diskon > 100:
                            print("Diskon harus antara 0-100%.")
                            continue
                    except ValueError:
                        print("Input diskon tidak valid.")
                        continue
                    
                    hasil, waktu = ukur_waktu(hitung_total_dengan_diskon, harga, diskon)
                    print(f"\nTotal belanja dengan diskon {diskon}% (O(n)): Rp{hasil:.2f}, Waktu: {waktu:.6f} ms")
                
                elif algoritma == 3:
                    # Menggunakan ukur_waktu dengan fungsi lambda untuk menangani multiple return values
                    (total, pasangan_ditemukan), waktu = ukur_waktu(
                        lambda: hitung_total_dengan_promosi_bundling_on2(harga, produk, pasangan_bundling)
                    )
                    print(f"\nTotal belanja dengan promosi bundling (O(n²)): Rp{total:.2f}, Waktu: {waktu:.6f} ms")
                    
                    # Tampilkan informasi tentang bundling yang ditemukan
                    if pasangan_ditemukan:
                        print("\nPasangan bundling yang ditemukan:")
                        for i, j, kunci1, kunci2, diskon_persen, diskon in pasangan_ditemukan:
                            print(f"  - {produk[i]} (Rp{harga[i]}) + {produk[j]} (Rp{harga[j]})")
                            print(f"    Promosi: '{kunci1}' + '{kunci2}' = Diskon {diskon_persen}%")
                            print(f"    Diskon: Rp{diskon:.2f}")
                    else:
                        print("\nTidak ada pasangan bundling yang ditemukan.")
                
                elif algoritma == 4:
                    hasil_o1, waktu_o1 = ukur_waktu(hitung_total_sederhana, harga)
                    print(f"Total belanja (O(1)): Rp{hasil_o1:.2f}, Waktu: {waktu_o1:.6f} ms")
                    
                    try:
                        diskon = float(input("Masukkan persentase diskon (%): "))
                        if diskon < 0 or diskon > 100:
                            print("Diskon harus antara 0-100%.")
                            continue
                    except ValueError:
                        print("Input diskon tidak valid.")
                        continue
                    
                    hasil_on, waktu_on = ukur_waktu(hitung_total_dengan_diskon, harga, diskon)
                    print(f"Total belanja dengan diskon {diskon}% (O(n)): Rp{hasil_on:.2f}, Waktu: {waktu_on:.6f} ms")
                    
                    # Menggunakan ukur_waktu dengan fungsi lambda untuk menangani multiple return values
                    (hasil_on2, pasangan_ditemukan), waktu_on2 = ukur_waktu(
                        lambda: hitung_total_dengan_promosi_bundling_on2(harga, produk, pasangan_bundling)
                    )
                    print(f"Total belanja dengan promosi bundling (O(n²)): Rp{hasil_on2:.2f}, Waktu: {waktu_on2:.6f} ms")
                    
                    # Tampilkan informasi tentang bundling yang ditemukan
                    if pasangan_ditemukan:
                        print("\nPasangan bundling yang ditemukan:")
                        for i, j, kunci1, kunci2, diskon_persen, diskon in pasangan_ditemukan:
                            print(f"  - {produk[i]} (Rp{harga[i]}) + {produk[j]} (Rp{harga[j]})")
                            print(f"    Promosi: '{kunci1}' + '{kunci2}' = Diskon {diskon_persen}%")
                            print(f"    Diskon: Rp{diskon:.2f}")
                    else:
                        print("\nTidak ada pasangan bundling yang ditemukan.")
            
            elif pilihan == 7:
                print("\nUji Performa Algoritma dengan Data Acak")
                ukuran_data = [10, 100, 1000, 10000]
                
                # Gunakan pasangan bundling yang diinput atau default
                bundling_test = pasangan_bundling if pasangan_bundling else [("shampoo", "conditioner", 20)]
                
                print("\nPerbandingan Waktu Eksekusi:")
                print("| Ukuran Data | O(1) (ms) | O(n) (ms) | O(n²) (ms) |")
                print("|-------------|-----------|-----------|------------|")
                
                for ukuran in ukuran_data:
                    nama_produk_test, harga_test = buat_data_uji(ukuran)
                    
                    _, waktu_o1 = ukur_waktu(hitung_total_sederhana, harga_test)
                    _, waktu_on = ukur_waktu(hitung_total_dengan_diskon, harga_test, 10)
                    
                    # Menggunakan fungsi lambda untuk hanya mendapatkan hasil pertama dari multiple return
                    _, waktu_on2 = ukur_waktu(
                        lambda: hitung_total_dengan_promosi_bundling_on2(harga_test, nama_produk_test, bundling_test)[0]
                    )
                    
                    print(f"| {ukuran:11d} | {waktu_o1:9.6f} | {waktu_on:9.6f} | {waktu_on2:10.6f} |")
            
            elif pilihan == 8:
                print("Terima kasih telah menggunakan program ini. Sampai jumpa!")
                break
            
            else:
                print("Pilihan tidak valid. Masukkan angka 1-8.")
        
        except ValueError:
            print("Input tidak valid. Masukkan angka 1-8.")

# Memulai program
if __name__ == "__main__":
    print("Selamat datang di Program Menghitung Total Belanja!")
    print("Program ini mendemonstrasikan perbedaan kompleksitas algoritma.")
    menu_utama()
