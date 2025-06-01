# Parent class Akun
class Akun:
    def login(self):
        # Ini adalah metode umum yang akan dioverride oleh subclass
        print("Login sebagai akun umum")

# Subclass Admin mewarisi dari Akun
class Admin(Akun):
    def login(self):
        # Override metode login untuk Admin
        print("Login sebagai Admin dengan autentikasi dua faktor")

# Subclass UserBiasa mewarisi dari Akun
class UserBiasa(Akun):
    def login(self):
        # Override metode login untuk User Biasa
        print("Login sebagai User Biasa dengan username dan password")

# Subclass Guest mewarisi dari Akun
class Guest(Akun):
    def login(self):
        # Override metode login untuk Guest
        print("Login sebagai Guest tanpa autentikasi")

# Polimorfisme: menggunakan list yang berisi objek dari berbagai subclass
daftar_akun = [Admin(), UserBiasa(), Guest()]

# Melakukan iterasi dan memanggil metode login
# Di sinilah polimorfisme bekerja — Python akan secara otomatis
# memanggil versi metode login() yang sesuai dengan tipe objeknya
for akun in daftar_akun:
    akun.login()
