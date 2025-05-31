import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import uuid

class Buku:
    def __init__(self, judul, penulis, isbn, tahun_terbit):
        self.judul = judul
        self.penulis = penulis
        self.isbn = isbn
        self.tahun_terbit = tahun_terbit
        self.tersedia = True

    def __str__(self):
        status = "Tersedia" if self.tersedia else "Dipinjam"
        return f"{self.judul} oleh {self.penulis} ({self.tahun_terbit}) - {status}"


class Pelanggan:
    def __init__(self, id_pelanggan, nama, alamat, no_telepon):
        self.id_pelanggan = id_pelanggan
        self.nama = nama
        self.alamat = alamat
        self.no_telepon = no_telepon
        self.buku_dipinjam = []

    def __str__(self):
        return f"{self.nama} (ID: {self.id_pelanggan})"


class Transaksi:
    def __init__(self, id_transaksi, pelanggan, buku, tanggal_pinjam):
        self.id_transaksi = id_transaksi
        self.pelanggan = pelanggan
        self.buku = buku
        self.tanggal_pinjam = tanggal_pinjam
        self.tanggal_kembali = tanggal_pinjam + timedelta(days=14)  # Asumsi peminjaman 14 hari
        self.status = "Dipinjam"  # Dipinjam atau Dikembalikan

    def __str__(self):
        return f"ID: {self.id_transaksi} - {self.pelanggan.nama} meminjam '{self.buku.judul}' pada {self.tanggal_pinjam.strftime('%d/%m/%Y')} - Status: {self.status}"


class Perpustakaan:
    def __init__(self):
        self.koleksi_buku = []
        self.daftar_pelanggan = []
        self.transaksi = []

    def tambah_buku(self, buku):
        self.koleksi_buku.append(buku)
        return True

    def cari_buku_berdasarkan_isbn(self, isbn):
        for buku in self.koleksi_buku:
            if buku.isbn == isbn:
                return buku
        return None

    def daftar_buku_tersedia(self):
        return [buku for buku in self.koleksi_buku if buku.tersedia]

    def tambah_pelanggan(self, pelanggan):
        self.daftar_pelanggan.append(pelanggan)
        return True

    def cari_pelanggan(self, id_pelanggan):
        for pelanggan in self.daftar_pelanggan:
            if pelanggan.id_pelanggan == id_pelanggan:
                return pelanggan
        return None

    def pinjam_buku(self, id_pelanggan, isbn):
        pelanggan = self.cari_pelanggan(id_pelanggan)
        buku = self.cari_buku_berdasarkan_isbn(isbn)
        
        if not pelanggan:
            return False, "Pelanggan tidak ditemukan"
        
        if not buku:
            return False, "Buku tidak ditemukan"
        
        if not buku.tersedia:
            return False, "Buku tidak tersedia"
        
        # Proses peminjaman
        id_transaksi = str(uuid.uuid4())[:8]  # Buat ID transaksi sederhana
        transaksi_baru = Transaksi(id_transaksi, pelanggan, buku, datetime.now())
        self.transaksi.append(transaksi_baru)
        
        buku.tersedia = False
        pelanggan.buku_dipinjam.append(buku)
        
        return True, id_transaksi

    def kembalikan_buku(self, id_transaksi):
        for transaksi in self.transaksi:
            if transaksi.id_transaksi == id_transaksi and transaksi.status == "Dipinjam":
                transaksi.status = "Dikembalikan"
                transaksi.buku.tersedia = True
                
                # Hapus buku dari daftar buku yang dipinjam oleh pelanggan
                if transaksi.buku in transaksi.pelanggan.buku_dipinjam:
                    transaksi.pelanggan.buku_dipinjam.remove(transaksi.buku)
                
                return True
        
        return False


class AppPerpustakaan(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x600")
        self.perpustakaan = Perpustakaan()
        
        # Inisialisasi data dummy
        self.inisialisasi_data_dummy()
        
        # Setup UI
        self.setup_ui()

    def inisialisasi_data_dummy(self):
        # Tambah beberapa buku
        buku1 = Buku("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "1", 1997)
        buku2 = Buku("To Kill a Mockingbird", "Harper Lee", "2", 1960)
        buku3 = Buku("The Great Gatsby", "F. Scott Fitzgerald", "3", 1925)
        
        self.perpustakaan.tambah_buku(buku1)
        self.perpustakaan.tambah_buku(buku2)
        self.perpustakaan.tambah_buku(buku3)
        
        # Tambah beberapa pelanggan
        pelanggan1 = Pelanggan("P001", "Budi Santoso", "Jl. Merdeka No. 10", "08123456789")
        pelanggan2 = Pelanggan("P002", "Dewi Lestari", "Jl. Pahlawan No. 25", "08198765432")
        
        self.perpustakaan.tambah_pelanggan(pelanggan1)
        self.perpustakaan.tambah_pelanggan(pelanggan2)

    def setup_ui(self):
        # Membuat notebook (tab)
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab untuk Manajemen Buku
        tab_buku = ttk.Frame(notebook)
        notebook.add(tab_buku, text="Manajemen Buku")
        self.setup_tab_buku(tab_buku)
        
        # Tab untuk Manajemen Pelanggan
        tab_pelanggan = ttk.Frame(notebook)
        notebook.add(tab_pelanggan, text="Manajemen Pelanggan")
        self.setup_tab_pelanggan(tab_pelanggan)
        
        # Tab untuk Transaksi
        tab_transaksi = ttk.Frame(notebook)
        notebook.add(tab_transaksi, text="Transaksi")
        self.setup_tab_transaksi(tab_transaksi)
        
        # Tab untuk Laporan
        tab_laporan = ttk.Frame(notebook)
        notebook.add(tab_laporan, text="Laporan Transaksi")
        self.setup_tab_laporan(tab_laporan)

    def setup_tab_buku(self, parent):
        # Frame untuk form tambah buku
        frame_form = ttk.LabelFrame(parent, text="Tambah Buku Baru")
        frame_form.pack(fill="x", padx=10, pady=10)
        
        # Form fields
        ttk.Label(frame_form, text="Judul:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_judul = ttk.Entry(frame_form, width=40)
        self.entry_judul.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Penulis:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_penulis = ttk.Entry(frame_form, width=40)
        self.entry_penulis.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="ISBN:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_isbn = ttk.Entry(frame_form, width=40)
        self.entry_isbn.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Tahun Terbit:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_tahun = ttk.Entry(frame_form, width=40)
        self.entry_tahun.grid(row=3, column=1, padx=5, pady=5)
        
        # Tombol Tambah
        btn_tambah = ttk.Button(frame_form, text="Tambah Buku", command=self.tambah_buku)
        btn_tambah.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame untuk daftar buku
        frame_daftar = ttk.LabelFrame(parent, text="Daftar Buku")
        frame_daftar.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview untuk menampilkan buku
        columns = ("judul", "penulis", "isbn", "tahun", "status")
        self.tree_buku = ttk.Treeview(frame_daftar, columns=columns, show="headings")
        
        # Definisikan header untuk setiap kolom
        self.tree_buku.heading("judul", text="Judul")
        self.tree_buku.heading("penulis", text="Penulis")
        self.tree_buku.heading("isbn", text="ISBN")
        self.tree_buku.heading("tahun", text="Tahun Terbit")
        self.tree_buku.heading("status", text="Status")
        
        # Atur lebar kolom
        self.tree_buku.column("judul", width=200)
        self.tree_buku.column("penulis", width=150)
        self.tree_buku.column("isbn", width=100)
        self.tree_buku.column("tahun", width=100)
        self.tree_buku.column("status", width=100)
        
        # Tambahkan scrollbar
        scrollbar = ttk.Scrollbar(frame_daftar, orient="vertical", command=self.tree_buku.yview)
        self.tree_buku.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree_buku.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tombol refresh
        btn_refresh = ttk.Button(frame_daftar, text="Refresh", command=self.refresh_daftar_buku)
        btn_refresh.pack(pady=10)
        
        # Isi daftar buku pertama kali
        self.refresh_daftar_buku()

    def setup_tab_pelanggan(self, parent):
        # Frame untuk form tambah pelanggan
        frame_form = ttk.LabelFrame(parent, text="Tambah Pelanggan Baru")
        frame_form.pack(fill="x", padx=10, pady=10)
        
        # Form fields
        ttk.Label(frame_form, text="ID Pelanggan:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id_pelanggan = ttk.Entry(frame_form, width=40)
        self.entry_id_pelanggan.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Nama:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_nama_pelanggan = ttk.Entry(frame_form, width=40)
        self.entry_nama_pelanggan.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Alamat:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_alamat_pelanggan = ttk.Entry(frame_form, width=40)
        self.entry_alamat_pelanggan.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="No. Telepon:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_telepon_pelanggan = ttk.Entry(frame_form, width=40)
        self.entry_telepon_pelanggan.grid(row=3, column=1, padx=5, pady=5)
        
        # Tombol Tambah
        btn_tambah = ttk.Button(frame_form, text="Tambah Pelanggan", command=self.tambah_pelanggan)
        btn_tambah.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame untuk daftar pelanggan
        frame_daftar = ttk.LabelFrame(parent, text="Daftar Pelanggan")
        frame_daftar.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview untuk menampilkan pelanggan
        columns = ("id", "nama", "alamat", "telepon", "buku_dipinjam")
        self.tree_pelanggan = ttk.Treeview(frame_daftar, columns=columns, show="headings")
        
        # Definisikan header untuk setiap kolom
        self.tree_pelanggan.heading("id", text="ID")
        self.tree_pelanggan.heading("nama", text="Nama")
        self.tree_pelanggan.heading("alamat", text="Alamat")
        self.tree_pelanggan.heading("telepon", text="No. Telepon")
        self.tree_pelanggan.heading("buku_dipinjam", text="Jumlah Buku Dipinjam")
        
        # Atur lebar kolom
        self.tree_pelanggan.column("id", width=50)
        self.tree_pelanggan.column("nama", width=150)
        self.tree_pelanggan.column("alamat", width=200)
        self.tree_pelanggan.column("telepon", width=100)
        self.tree_pelanggan.column("buku_dipinjam", width=150)
        
        # Tambahkan scrollbar
        scrollbar = ttk.Scrollbar(frame_daftar, orient="vertical", command=self.tree_pelanggan.yview)
        self.tree_pelanggan.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree_pelanggan.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tombol refresh
        btn_refresh = ttk.Button(frame_daftar, text="Refresh", command=self.refresh_daftar_pelanggan)
        btn_refresh.pack(pady=10)
        
        # Isi daftar pelanggan pertama kali
        self.refresh_daftar_pelanggan()

    def setup_tab_transaksi(self, parent):
        # Frame untuk form peminjaman buku
        frame_pinjam = ttk.LabelFrame(parent, text="Peminjaman Buku")
        frame_pinjam.pack(fill="x", padx=10, pady=10)
        
        # Form fields untuk peminjaman
        ttk.Label(frame_pinjam, text="ID Pelanggan:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_pinjam_id_pelanggan = ttk.Entry(frame_pinjam, width=40)
        self.entry_pinjam_id_pelanggan.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_pinjam, text="ISBN Buku:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_pinjam_isbn = ttk.Entry(frame_pinjam, width=40)
        self.entry_pinjam_isbn.grid(row=1, column=1, padx=5, pady=5)
        
        # Tombol Pinjam
        btn_pinjam = ttk.Button(frame_pinjam, text="Pinjam Buku", command=self.pinjam_buku)
        btn_pinjam.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame untuk form pengembalian buku
        frame_kembali = ttk.LabelFrame(parent, text="Pengembalian Buku")
        frame_kembali.pack(fill="x", padx=10, pady=10)
        
        # Form fields untuk pengembalian
        ttk.Label(frame_kembali, text="ID Transaksi:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_kembali_id_transaksi = ttk.Entry(frame_kembali, width=40)
        self.entry_kembali_id_transaksi.grid(row=0, column=1, padx=5, pady=5)
        
        # Tombol Kembali
        btn_kembali = ttk.Button(frame_kembali, text="Kembalikan Buku", command=self.kembalikan_buku)
        btn_kembali.grid(row=1, column=0, columnspan=2, pady=10)

    def setup_tab_laporan(self, parent):
        # Frame untuk laporan transaksi
        frame_laporan = ttk.LabelFrame(parent, text="Daftar Transaksi")
        frame_laporan.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview untuk menampilkan transaksi
        columns = ("id", "pelanggan", "buku", "tanggal_pinjam", "tanggal_kembali", "status")
        self.tree_transaksi = ttk.Treeview(frame_laporan, columns=columns, show="headings")
        
        # Definisikan header untuk setiap kolom
        self.tree_transaksi.heading("id", text="ID Transaksi")
        self.tree_transaksi.heading("pelanggan", text="Pelanggan")
        self.tree_transaksi.heading("buku", text="Buku")
        self.tree_transaksi.heading("tanggal_pinjam", text="Tanggal Pinjam")
        self.tree_transaksi.heading("tanggal_kembali", text="Tanggal Kembali")
        self.tree_transaksi.heading("status", text="Status")
        
        # Atur lebar kolom
        self.tree_transaksi.column("id", width=100)
        self.tree_transaksi.column("pelanggan", width=150)
        self.tree_transaksi.column("buku", width=200)
        self.tree_transaksi.column("tanggal_pinjam", width=100)
        self.tree_transaksi.column("tanggal_kembali", width=100)
        self.tree_transaksi.column("status", width=100)
        
        # Tambahkan scrollbar
        scrollbar = ttk.Scrollbar(frame_laporan, orient="vertical", command=self.tree_transaksi.yview)
        self.tree_transaksi.configure(yscrollcommand=scrollbar.set)
        
        # Pack komponen
        self.tree_transaksi.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tombol refresh
        btn_refresh = ttk.Button(frame_laporan, text="Refresh", command=self.refresh_daftar_transaksi)
        btn_refresh.pack(pady=10)
        
        # Isi daftar transaksi pertama kali
        self.refresh_daftar_transaksi()

    def tambah_buku(self):
        try:
            judul = self.entry_judul.get()
            penulis = self.entry_penulis.get()
            isbn = self.entry_isbn.get()
            tahun = int(self.entry_tahun.get())
            
            if not (judul and penulis and isbn and tahun):
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            
            # Cek apakah ISBN sudah ada
            if self.perpustakaan.cari_buku_berdasarkan_isbn(isbn):
                messagebox.showerror("Error", f"Buku dengan ISBN {isbn} sudah ada dalam sistem!")
                return
            
            buku_baru = Buku(judul, penulis, isbn, tahun)
            if self.perpustakaan.tambah_buku(buku_baru):
                messagebox.showinfo("Sukses", f"Buku '{judul}' berhasil ditambahkan!")
                
                # Clear form
                self.entry_judul.delete(0, tk.END)
                self.entry_penulis.delete(0, tk.END)
                self.entry_isbn.delete(0, tk.END)
                self.entry_tahun.delete(0, tk.END)
                
                # Refresh daftar buku
                self.refresh_daftar_buku()
            else:
                messagebox.showerror("Error", "Gagal menambahkan buku!")
        except ValueError:
            messagebox.showerror("Error", "Tahun terbit harus berupa angka!")

    def refresh_daftar_buku(self):
        # Clear daftar buku
        for item in self.tree_buku.get_children():
            self.tree_buku.delete(item)
        
        # Isi ulang daftar buku
        for buku in self.perpustakaan.koleksi_buku:
            status = "Tersedia" if buku.tersedia else "Dipinjam"
            self.tree_buku.insert("", "end", values=(buku.judul, buku.penulis, buku.isbn, buku.tahun_terbit, status))

    def tambah_pelanggan(self):
        id_pelanggan = self.entry_id_pelanggan.get()
        nama = self.entry_nama_pelanggan.get()
        alamat = self.entry_alamat_pelanggan.get()
        telepon = self.entry_telepon_pelanggan.get()
        
        if not (id_pelanggan and nama and alamat and telepon):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        
        # Cek apakah ID pelanggan sudah ada
        if self.perpustakaan.cari_pelanggan(id_pelanggan):
            messagebox.showerror("Error", f"Pelanggan dengan ID {id_pelanggan} sudah ada dalam sistem!")
            return
        
        pelanggan_baru = Pelanggan(id_pelanggan, nama, alamat, telepon)
        if self.perpustakaan.tambah_pelanggan(pelanggan_baru):
            messagebox.showinfo("Sukses", f"Pelanggan '{nama}' berhasil ditambahkan!")
            
            # Clear form
            self.entry_id_pelanggan.delete(0, tk.END)
            self.entry_nama_pelanggan.delete(0, tk.END)
            self.entry_alamat_pelanggan.delete(0, tk.END)
            self.entry_telepon_pelanggan.delete(0, tk.END)
            
            # Refresh daftar pelanggan
            self.refresh_daftar_pelanggan()
        else:
            messagebox.showerror("Error", "Gagal menambahkan pelanggan!")

    def refresh_daftar_pelanggan(self):
        # Clear daftar pelanggan
        for item in self.tree_pelanggan.get_children():
            self.tree_pelanggan.delete(item)
        
        # Isi ulang daftar pelanggan
        for pelanggan in self.perpustakaan.daftar_pelanggan:
            jumlah_buku = len(pelanggan.buku_dipinjam)
            self.tree_pelanggan.insert("", "end", values=(pelanggan.id_pelanggan, pelanggan.nama, pelanggan.alamat, pelanggan.no_telepon, jumlah_buku))

    def pinjam_buku(self):
        id_pelanggan = self.entry_pinjam_id_pelanggan.get()
        isbn = self.entry_pinjam_isbn.get()
        
        if not (id_pelanggan and isbn):
            messagebox.showerror("Error", "ID Pelanggan dan ISBN Buku harus diisi!")
            return
        
        sukses, pesan = self.perpustakaan.pinjam_buku(id_pelanggan, isbn)
        
        if sukses:
            messagebox.showinfo("Sukses", f"Buku berhasil dipinjam! ID Transaksi: {pesan}")
            # Clear form
            self.entry_pinjam_id_pelanggan.delete(0, tk.END)
            self.entry_pinjam_isbn.delete(0, tk.END)
            # Refresh daftar buku dan transaksi
            self.refresh_daftar_buku()
            self.refresh_daftar_transaksi()
            self.refresh_daftar_pelanggan()
        else:
            messagebox.showerror("Error", pesan)

    def kembalikan_buku(self):
        id_transaksi = self.entry_kembali_id_transaksi.get()
        
        if not id_transaksi:
            messagebox.showerror("Error", "ID Transaksi harus diisi!")
            return
        
        if self.perpustakaan.kembalikan_buku(id_transaksi):
            messagebox.showinfo("Sukses", "Buku berhasil dikembalikan!")
            # Clear form
            self.entry_kembali_id_transaksi.delete(0, tk.END)
            # Refresh daftar buku dan transaksi
            self.refresh_daftar_buku()
            self.refresh_daftar_transaksi()
            self.refresh_daftar_pelanggan()
        else:
            messagebox.showerror("Error", "Gagal mengembalikan buku! Periksa ID Transaksi.")

    def refresh_daftar_transaksi(self):
        # Clear daftar transaksi
        for item in self.tree_transaksi.get_children():
            self.tree_transaksi.delete(item)
        
        # Isi ulang daftar transaksi
        for transaksi in self.perpustakaan.transaksi:
            tanggal_pinjam = transaksi.tanggal_pinjam.strftime("%d/%m/%Y")
            tanggal_kembali = transaksi.tanggal_kembali.strftime("%d/%m/%Y")
            self.tree_transaksi.insert("", "end", values=(
                transaksi.id_transaksi,
                transaksi.pelanggan.nama,
                transaksi.buku.judul,
                tanggal_pinjam,
                tanggal_kembali,
                transaksi.status
            ))


if __name__ == "__main__":
    app = AppPerpustakaan()
    app.mainloop()
