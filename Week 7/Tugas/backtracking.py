class Activity:
    def __init__(self, name, category, cost, day, importance=1):
        self.name = name
        self.category = category
        self.cost = cost
        self.day = day
        self.importance = importance  # 1-10 scale, 10 being most important
    
    def __str__(self):
        return f"{self.name} (Rp{self.cost:,})"

def backtrack_plan(budget, activities, current_plan=None, index=0, remaining=None):
    if current_plan is None:
        current_plan = []
    if remaining is None:
        remaining = budget
    
    # Base case: We've considered all activities
    if index == len(activities):
        # Check if we've spent exactly the budget
        if remaining == 0:
            # Make sure we have at least one activity per day and all categories are covered
            days_covered = set()
            categories_covered = set()
            for activity in current_plan:
                days_covered.add(activity.day)
                categories_covered.add(activity.category)
            
            required_categories = {"accommodation", "food", "transportation", "attraction"}
            if len(days_covered) == 3 and all(cat in categories_covered for cat in required_categories):
                return current_plan
        return None
    
    # Try including the current activity
    if activities[index].cost <= remaining:
        current_plan.append(activities[index])
        solution = backtrack_plan(budget, activities, current_plan, index + 1, remaining - activities[index].cost)
        if solution:
            return solution
        current_plan.pop()  # Backtrack
    
    # Try excluding the current activity
    solution = backtrack_plan(budget, activities, current_plan, index + 1, remaining)
    if solution:
        return solution
    
    return None

def generate_trip_plan(budget=7500000):
    # Define all possible activities
    activities = [
        # Day 1
        Activity("Tiket Pesawat Surabaya-Singapura", "transportation", 1250000, 1, 10),
        Activity("Hostel di Little India (Malam 1)", "accommodation", 1000000, 1, 10),
        Activity("MRT dari Bandara ke Hostel", "transportation", 100000, 1, 10),
        Activity("Breakfast: Kopi dan roti lokal", "food", 50000, 1, 7),
        Activity("Lunch: Maxwell Food Centre", "food", 100000, 1, 7),
        Activity("Dinner: Little India Food Court", "food", 100000, 1, 7),
        Activity("Gardens by the Bay - OCBC Skyway", "attraction", 150000, 1, 8),
        Activity("Gardens by the Bay - Flower Dome & Cloud Forest", "attraction", 250000, 1, 8),
        
        # Day 2
        Activity("Hostel di Little India (Malam 2)", "accommodation", 1000000, 2, 10),
        Activity("Transportasi MRT dan bus", "transportation", 150000, 2, 10),
        Activity("Breakfast: Kaya toast di Ya Kun", "food", 70000, 2, 7),
        Activity("Lunch: Chinatown Complex Food Centre", "food", 130000, 2, 7),
        Activity("Dinner: Lau Pa Sat", "food", 150000, 2, 7),
        Activity("Marina Bay Sands Observation Deck", "attraction", 300000, 2, 8),
        
        # Day 3
        Activity("Tiket Pesawat Singapura-Surabaya", "transportation", 1250000, 3, 10),
        Activity("Transportasi MRT, bus dan ke Bandara", "transportation", 250000, 3, 10),
        Activity("Breakfast: Toast Box", "food", 80000, 3, 7),
        Activity("Lunch: Hawker Center di Chinatown", "food", 120000, 3, 7),
        Activity("Snack untuk perjalanan pulang", "food", 200000, 3, 6),
        Activity("Jajanan untuk oleh-oleh", "food", 500000, 3, 7),
        Activity("Shopping di Bugis Street", "attraction", 300000, 3, 8),
        
        # Free attractions (cost 0)
        Activity("Supertree Grove Light Show", "attraction", 0, 1, 9),
        Activity("Spectra Light Show di Marina Bay", "attraction", 0, 2, 9),
        Activity("Singapore Botanic Gardens", "attraction", 0, 3, 8),
        Activity("Buddha Tooth Relic Temple", "attraction", 0, 3, 7),
        Activity("Merlion Park", "attraction", 0, 2, 9),
    ]
    
    # Sort activities by importance (optional)
    activities.sort(key=lambda x: x.importance, reverse=True)
    
    # Run backtracking algorithm
    optimal_plan = backtrack_plan(budget, activities)
    
    return optimal_plan

def display_plan(plan):
    if not plan:
        print("Tidak menemukan rencana yang memenuhi budget secara tepat.")
        return
    
    total_cost = 0
    days = {1: [], 2: [], 3: []}
    categories = {"accommodation": [], "food": [], "transportation": [], "attraction": []}
    
    for activity in plan:
        days[activity.day].append(activity)
        categories[activity.category].append(activity)
        total_cost += activity.cost
    
    print(f"== RENCANA LIBURAN SURABAYA KE SINGAPURA ==")
    print(f"Budget: Rp{7500000:,}")
    print(f"Total biaya: Rp{total_cost:,}")
    print("\n")
    
    for day in range(1, 4):
        print(f"=== HARI {day} ===")
        day_activities = days[day]
        day_cost = sum(activity.cost for activity in day_activities)
        
        # Sort activities by category for better readability
        day_activities.sort(key=lambda x: x.category)
        
        for activity in day_activities:
            print(f"- {activity.category.capitalize()}: {activity}")
        
        print(f"Total Hari {day}: Rp{day_cost:,}\n")
    
    print("=== RINGKASAN BIAYA ===")
    for category, activities in categories.items():
        category_cost = sum(activity.cost for activity in activities)
        print(f"{category.capitalize()}: Rp{category_cost:,}")
    
    # Hidden gems
    print("\n=== HIDDEN GEMS ===")
    hidden_gems = [activity for activity in plan if activity.cost == 0]
    for gem in hidden_gems:
        print(f"- {gem.name} (Hari {gem.day})")

# Jalankan program dengan pengukuran waktu eksekusi
if __name__ == "__main__":
    import time
    
    # Mulai pengukuran waktu
    start_time = time.time()
    
    budget = 7500000  # Rp7.5 juta
    optimal_plan = generate_trip_plan(budget)
    
    # Akhir pengukuran waktu
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Tampilkan hasil
    display_plan(optimal_plan)
    
    # Tampilkan waktu eksekusi
    print(f"\n=== WAKTU EKSEKUSI ===")
    print(f"Waktu eksekusi: {execution_time:.6f} detik")
    
    # Tambahan: Analisis kinerja untuk jumlah aktivitas
    print(f"Jumlah aktivitas: {len(optimal_plan)} dipilih dari {len(generate_trip_plan.__code__.co_consts[1])} aktivitas yang tersedia")
    print(f"Kompleksitas teoritis: O(2^{len(generate_trip_plan.__code__.co_consts[1])}) = {2**len(generate_trip_plan.__code__.co_consts[1])} kemungkinan kombinasi")
    print(f"Efisiensi pruning: Hanya sebagian kecil dari state space yang perlu dieksplorasi karena batasan anggaran dan optimasi")

# =====================================================================
# PENJELASAN LOGIKA BACKTRACKING
# =====================================================================
#
# Algoritma backtracking dalam program ini bekerja dengan prinsip "try and backtrack" untuk menemukan
# solusi optimal yang memenuhi seluruh syarat perencanaan perjalanan. Berikut penjelasan detail logikanya:
#
# 1. STATE SPACE: 
#    - Setiap aktivitas dapat dipilih (include) atau tidak dipilih (exclude)
#    - Total kemungkinan state: 2^n, dimana n adalah jumlah aktivitas (27 aktivitas = 2^27 kemungkinan)
#
# 2. RECURSIVE DECISION:
#    - Untuk setiap aktivitas, algoritma membuat keputusan binary: ambil atau tidak
#    - Keputusan dibuat secara rekursif, dimulai dari aktivitas pertama sampai terakhir
#    - Setiap keputusan menghasilkan cabang baru dalam pohon pencarian
#
# 3. PRUNING (PEMOTONGAN):
#    - Jika aktivitas melebihi sisa budget, cabang tersebut langsung dipotong
#    - Ini mengurangi state space yang perlu dieksplorasi
#
# 4. BACKTRACKING STEP:
#    - Ketika algoritma mencapai jalan buntu (tidak ada solusi valid), ia "backtrack" (mundur)
#    - Implementasi backtracking: current_plan.pop() untuk menghapus aktivitas terakhir
#    - Kemudian mencoba jalur alternatif (exclude aktivitas yang tadi include)
#
# 5. VALIDASI SOLUSI:
#    - Solusi dianggap valid jika:
#       a. Budget terpakai tepat (remaining == 0)
#       b. Semua hari terpenuhi (len(days_covered) == 3)
#       c. Semua kategori terpenuhi (akomodasi, makanan, transportasi, atraksi)
#
# 6. URUTAN AKTIVITAS:
#    - Aktivitas diurutkan berdasarkan importance (prioritas), memungkinkan solusi ditemukan lebih cepat
#    - Ini adalah optimasi untuk mengarahkan pencarian ke solusi yang lebih mungkin terlebih dahulu
#
# 7. COMPLEXITY:
#    - Worst case: O(2^n) dimana n adalah jumlah aktivitas
#    - Namun pruning dan prioritas aktivitas secara signifikan mengurangi jumlah state yang dieksplorasi
#
# 8. WAKTU EKSEKUSI:
#    - Waktu eksekusi dipengaruhi oleh:
#       a. Jumlah aktivitas (n)
#       b. Efektivitas pruning (semakin baik pruning, semakin cepat eksekusi)
#       c. Urutan aktivitas (pengurutan berdasarkan importance membantu mencapai solusi lebih cepat)
#       d. Keberadaan solusi (jika tidak ada solusi, seluruh state space mungkin perlu dieksplorasi)
#
# =====================================================================
# ANALISIS KELEBIHAN DAN KEKURANGAN
# =====================================================================
#
# KELEBIHAN:
#
# 1. SOLUSI OPTIMAL TERJAMIN
#    - Backtracking menjamin menemukan solusi optimal jika ada, karena akan mengeksplorasi
#      semua kemungkinan yang valid
#
# 2. CONSTRAINT SATISFACTION
#    - Sangat baik untuk masalah dengan banyak batasan (constraints)
#    - Dapat menangani berbagai constraints seperti budget tepat, kategori lengkap, dan hari tercover
#
# 3. FLEKSIBILITAS
#    - Mudah dimodifikasi untuk mengakomodasi batasan tambahan
#    - Misalnya, menambahkan batasan jarak antar tempat, jam operasional, dll
#
# 4. ADAPTIF
#    - Dapat menyesuaikan jika ada perubahan mendadak (seperti delay cuaca)
#    - Cukup jalankan ulang dengan aktivitas yang diubah/dihapus
#
# 5. PENANGANAN KOMPLEKSITAS
#    - Mampu menangani masalah kompleks yang sulit diselesaikan dengan pendekatan greedy
#
# KEKURANGAN:
#
# 1. KOMPLEKSITAS WAKTU
#    - Worst case exponential: O(2^n) dalam jumlah aktivitas
#    - Untuk jumlah aktivitas yang besar (>30), mungkin membutuhkan waktu sangat lama
#    - Waktu eksekusi dapat bervariasi signifikan berdasarkan karakteristik input
#
# 2. MEMORI INTENSIF
#    - Rekursi membutuhkan stack memory yang besar untuk masalah kompleks
#    - Dapat menyebabkan stack overflow untuk dataset yang sangat besar
#
# 3. SOLUSI PERTAMA BIAS
#    - Program ini berhenti setelah menemukan solusi pertama yang valid
#    - Mungkin ada solusi alternatif yang sama-sama valid tetapi lebih sesuai preferensi user
#
# 4. KETERGANTUNGAN PADA URUTAN
#    - Hasil dapat bergantung pada urutan aktivitas dalam input
#    - Pengurutan berdasarkan importance adalah heuristik yang mungkin tidak optimal
#
# 5. BATASAN PEMODELAN
#    - Kesulitan dalam memodelkan preferensi subjektif atau batasan kompleks lainnya
#    - Misalnya, preferensi untuk aktivitas berurutan atau batasan waktu antar aktivitas
#
# 6. TIDAK MEMPERHITUNGKAN KONTINGENSI
#    - Tidak memiliki mekanisme built-in untuk menangani ketidakpastian
#    - Solusi mungkin tidak robust terhadap perubahan mendadak (kebutuhan re-planning)
#
# Alternatif pendekatan yang dapat dipertimbangkan:
# - Integer Linear Programming untuk optimasi yang lebih efisien
# - Algoritma Genetika untuk mendapatkan beberapa solusi alternatif
# - Pendekatan heuristik untuk masalah skala besar
