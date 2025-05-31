# Dengan Polimorfisme
# Parent class Sensor dengan metode baca_data()
class Sensor:
    def baca_data(self):
        # Metode ini akan di-override oleh subclass
        raise NotImplementedError("Subkelas harus mengimplementasikan metode ini.")

# Subclass untuk Sensor Suhu
class Suhu(Sensor):
    def baca_data(self):
        return "Suhu: 27°C"

# Subclass untuk Sensor Kelembaban
class Kelembaban(Sensor):
    def baca_data(self):
        return "Kelembaban: 65%"

# Subclass untuk Sensor Cahaya
class Cahaya(Sensor):
    def baca_data(self):
        return "Cahaya: 300 lux"

# Daftar sensor yang terdiri dari berbagai jenis
sensor_list = [Suhu(), Kelembaban(), Cahaya()]

# Polimorfisme: Kita bisa memperlakukan semua objek sebagai tipe Sensor
for sensor in sensor_list:
    print(sensor.baca_data())

# -----------------------
# PENJELASAN:
# Meskipun setiap objek (Suhu, Kelembaban, Cahaya) merupakan instance dari subclass yang berbeda,
# kita memperlakukan semuanya sebagai instance dari class Sensor.
# Method baca_data() yang tepat akan dipanggil sesuai dengan jenis objeknya (runtime dispatch).
