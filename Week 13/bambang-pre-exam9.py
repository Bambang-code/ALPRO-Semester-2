# Parent class Laporan
class Laporan:
    def generate(self):
        # Method ini akan dioverride oleh subclass
        print("Membuat laporan umum...")

# Subclass Keuangan mewarisi dari Laporan
class Keuangan(Laporan):
    def generate(self):
        # Override method generate() untuk laporan keuangan
        print("Menghasilkan Laporan Keuangan dalam format PDF...")

# Subclass Penjualan mewarisi dari Laporan
class Penjualan(Laporan):
    def generate(self):
        # Override method generate() untuk laporan penjualan
        print("Menghasilkan Laporan Penjualan dalam format Excel...")

# Subclass Proyek mewarisi dari Laporan
class Proyek(Laporan):
    def generate(self):
        # Override method generate() untuk laporan proyek
        print("Menghasilkan Laporan Proyek dalam format Word...")

# Menggunakan polimorfisme: membuat list objek dari berbagai subclass
daftar_laporan = [Keuangan(), Penjualan(), Proyek()]

# Melakukan iterasi dan memanggil method generate()
for laporan in daftar_laporan:
    # Di sini polimorfisme terjadi: meskipun semua objek dianggap bertipe Laporan,
    # Python akan memanggil versi metode generate() sesuai dengan kelas aslinya (subclass)
    laporan.generate()
