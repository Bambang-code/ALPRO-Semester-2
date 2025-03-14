import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class ProductSearchApp:
    def __init__(self):
        # Inisialisasi database produk
        self.products = self.generate_products(10000)  # Generate 10,000 produk
        # Urutkan produk berdasarkan nama untuk binary search
        self.sorted_products = sorted(self.products, key=lambda x: x['name'])
        
    def generate_products(self, n):
        """Membuat database produk secara acak"""
        categories = ['Elektronik', 'Pakaian', 'Makanan', 'Minuman', 'Perabotan', 'Kosmetik', 'Olahraga']
        products = []
        
        for i in range(n):
            product = {
                'id': i + 1,
                'name': f"Produk-{i + 1}",
                'category': random.choice(categories),
                'price': random.randint(10000, 1000000),
                'stock': random.randint(0, 100)
            }
            products.append(product)
        
        return products
    
    def linear_search(self, keyword):
        """Implementasi linear search O(n)"""
        start_time = time.time()
        results = []
        
        for product in self.products:
            if keyword.lower() in product['name'].lower():
                results.append(product)
                
        end_time = time.time()
        execution_time = end_time - start_time
        
        return results, execution_time
    
    def binary_search(self, keyword):
        """Implementasi binary search O(log n)"""
        start_time = time.time()
        results = []
        
        # Binary search hanya bekerja untuk pencarian yang persis sama
        # Untuk mencari substring, kita gunakan binary search untuk menemukan posisi awal
        # dan kemudian mencari substring di area sekitarnya
        
        # Implementasi modified binary search untuk substring
        left, right = 0, len(self.sorted_products) - 1
        found_index = -1
        
        # Mencari produk dengan nama yang persis sama dengan keyword
        while left <= right:
            mid = (left + right) // 2
            if self.sorted_products[mid]['name'].lower() == keyword.lower():
                found_index = mid
                break
            elif self.sorted_products[mid]['name'].lower() < keyword.lower():
                left = mid + 1
            else:
                right = mid - 1
        
        # Jika menemukan produk yang persis sama
        if found_index != -1:
            results.append(self.sorted_products[found_index])
            
            # Periksa produk serupa di sekitarnya (karena mungkin ada beberapa produk dengan nama yang sama)
            i = found_index - 1
            while i >= 0 and keyword.lower() in self.sorted_products[i]['name'].lower():
                results.append(self.sorted_products[i])
                i -= 1
                
            i = found_index + 1
            while i < len(self.sorted_products) and keyword.lower() in self.sorted_products[i]['name'].lower():
                results.append(self.sorted_products[i])
                i += 1
        else:
            # Jika tidak menemukan yang persis sama, lakukan pencarian linier dalam subset
            # untuk demonstrasi, kita terbatas pada 1000 item pertama
            subset = self.sorted_products[:1000]
            for product in subset:
                if keyword.lower() in product['name'].lower():
                    results.append(product)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return results, execution_time
    
    def run_comparison_test(self, keyword, dataset_sizes):
        """Menjalankan tes perbandingan waktu eksekusi"""
        table = PrettyTable()
        table.field_names = ["Ukuran Dataset", "Linear Search (detik)", "Binary Search (detik)", "Perbandingan (Binary/Linear)"]
        results = []
        
        for size in dataset_sizes:
            # Batasi dataset untuk pengujian
            self.products = self.generate_products(size)
            self.sorted_products = sorted(self.products, key=lambda x: x['name'])
            
            # Jalankan linear search
            _, linear_time = self.linear_search(keyword)
            
            # Jalankan binary search
            _, binary_time = self.binary_search(keyword)
            
            # Hitung perbandingan (jika linear_time tidak nol)
            if linear_time != 0:
                comparison = binary_time / linear_time
            else:
                comparison = "N/A"
                
            # Tambahkan hasil ke tabel
            table.add_row([size, f"{linear_time:.6f}", f"{binary_time:.6f}", f"{comparison:.6f}" if isinstance(comparison, float) else comparison])
            
            # Simpan hasil untuk grafik
            results.append({
                'size': size,
                'linear_time': linear_time,
                'binary_time': binary_time
            })
        
        return table, results
    
    def plot_comparison(self, results):
        """Membuat grafik perbandingan waktu eksekusi"""
        df = pd.DataFrame(results)
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['size'], df['linear_time'], 'ro-', label='Linear Search O(n)')
        plt.plot(df['size'], df['binary_time'], 'bo-', label='Binary Search O(log n)')
        plt.xlabel('Ukuran Dataset')
        plt.ylabel('Waktu Eksekusi (detik)')
        plt.title('Perbandingan Waktu Eksekusi Linear Search vs Binary Search')
        plt.legend()
        plt.grid(True)
        plt.savefig('search_comparison.png')
        plt.close()
    
    def print_products(self, products, max_results=5):
        """Menampilkan produk hasil pencarian"""
        if not products:
            print("Tidak ada produk yang cocok dengan kata kunci pencarian.")
            return
        
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Kategori", "Harga", "Stok"]
        
        for i, product in enumerate(products[:max_results]):
            table.add_row([
                product['id'],
                product['name'],
                product['category'],
                f"Rp {product['price']:,}",
                product['stock']
            ])
            
        print(f"Menampilkan {min(max_results, len(products))} dari {len(products)} hasil:")
        print(table)
        
    def search_menu(self):
        """Menu pencarian produk"""
        while True:
            print("\n===== APLIKASI PENCARIAN PRODUK ONLINE =====")
            print("1. Cari Produk (Linear Search)")
            print("2. Cari Produk (Binary Search)")
            print("3. Jalankan Perbandingan Algoritma")
            print("4. Keluar")
            
            choice = input("Pilih menu (1-4): ")
            
            if choice == '1':
                keyword = input("Masukkan kata kunci pencarian: ")
                results, execution_time = self.linear_search(keyword)
                print(f"\nHasil pencarian dengan Linear Search (waktu: {execution_time:.6f} detik):")
                self.print_products(results)
                
            elif choice == '2':
                keyword = input("Masukkan kata kunci pencarian: ")
                results, execution_time = self.binary_search(keyword)
                print(f"\nHasil pencarian dengan Binary Search (waktu: {execution_time:.6f} detik):")
                self.print_products(results)
                
            elif choice == '3':
                keyword = input("Masukkan kata kunci untuk pengujian: ")
                sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
                print("\nMenjalankan pengujian perbandingan waktu eksekusi...")
                print("(Ini mungkin memerlukan waktu beberapa saat untuk ukuran dataset besar)")
                
                table, results = self.run_comparison_test(keyword, sizes)
                print(table)
                
                print("\nMembuat grafik perbandingan...")
                self.plot_comparison(results)
                print("Grafik berhasil dibuat dan disimpan sebagai 'search_comparison.png'")
                
            elif choice == '4':
                print("Terima kasih telah menggunakan Aplikasi Pencarian Produk Online.")
                break
                
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

# Menjalankan aplikasi
if __name__ == "__main__":
    app = ProductSearchApp()
    app.search_menu()
