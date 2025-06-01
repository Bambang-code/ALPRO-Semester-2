# Parent class Notifikasi
class Notifikasi:
    def kirim(self):
        # Metode ini akan dioverride oleh subclass
        print("Mengirim notifikasi...")

# Subclass Email mewarisi Notifikasi
class Email(Notifikasi):
    def kirim(self):
        # Override metode kirim untuk notifikasi melalui Email
        print("Mengirim notifikasi melalui Email.")

# Subclass SMS mewarisi Notifikasi
class SMS(Notifikasi):
    def kirim(self):
        # Override metode kirim untuk notifikasi melalui SMS
        print("Mengirim notifikasi melalui SMS.")

# Subclass PushNotification mewarisi Notifikasi
class PushNotification(Notifikasi):
    def kirim(self):
        # Override metode kirim untuk notifikasi push
        print("Mengirim notifikasi melalui Push Notification.")

# Membuat daftar notifikasi dari berbagai jenis
daftar_notifikasi = [
    Email(),
    SMS(),
    PushNotification(),
    Email(),
    SMS()
]

# Mengirim notifikasi menggunakan polimorfisme
for notifikasi in daftar_notifikasi:
    # Polimorfisme digunakan di sini: walaupun tipe variabelnya adalah Notifikasi,
    # Python secara dinamis memanggil metode kirim() yang sesuai dengan jenis objeknya (Email, SMS, dll.)
    notifikasi.kirim()
