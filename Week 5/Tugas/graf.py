from collections import deque

# Representasi graf dalam bentuk adjacency list
graph = {
    0: [1], 1: [0, 2, 38], 2: [1, 3], 3: [2, 4], 4: [3, 5], 
    5: [4, 6], 6: [5, 7], 7: [6, 8], 8: [7, 9], 9: [8, 10], 
    10: [9, 11], 11: [10, 12], 12: [11, 13], 13: [12, 14], 
    14: [13, 15], 15: [14, 16], 16: [15, 17], 17: [16, 18], 
    18: [17, 19], 19: [18, 20], 20: [19, 21], 21: [20, 22], 
    22: [21, 23], 23: [22, 24], 24: [23, 25], 25: [24, 26], 
    26: [25, 27], 27: [26, 28], 28: [27, 29], 29: [28, 30], 
    30: [29, 31], 31: [30, 32], 32: [31, 33], 33: [32, 34], 
    34: [33, 35], 35: [34, 36], 36: [35, 37], 37: [36, 38], 
    38: [37, 1]
}

# Fungsi BFS untuk mencari jalur dari start ke goal
def bfs(start, goal):
    queue = deque([[start]])  # Antrian BFS menyimpan jalur
    visited = set()  # Set untuk menyimpan node yang sudah dikunjungi

    while queue:
        path = queue.popleft()  # Ambil jalur pertama dalam antrian
        node = path[-1]  # Ambil node terakhir dalam jalur

        if node == goal:
            return path  # Jika mencapai tujuan, kembalikan jalur

        if node not in visited:
            visited.add(node)  # Tandai node sebagai dikunjungi
            for neighbor in graph.get(node, []):
                new_path = list(path)  # Buat salinan jalur saat ini
                new_path.append(neighbor)  # Tambahkan node tetangga
                queue.append(new_path)  # Tambahkan ke antrian

    return None  # Tidak ada jalur ditemukan

# Fungsi DFS untuk mencari jalur dari start ke goal
def dfs(start, goal):
    stack = [[start]]  # Stack DFS menyimpan jalur
    visited = set()  # Set untuk menyimpan node yang sudah dikunjungi

    while stack:
        path = stack.pop()  # Ambil jalur terakhir dalam stack
        node = path[-1]  # Ambil node terakhir dalam jalur

        if node == goal:
            return path  # Jika mencapai tujuan, kembalikan jalur

        if node not in visited:
            visited.add(node)  # Tandai node sebagai dikunjungi
            for neighbor in graph.get(node, []):
                new_path = list(path)  # Buat salinan jalur saat ini
                new_path.append(neighbor)  # Tambahkan node tetangga
                stack.append(new_path)  # Tambahkan ke stack

    return None  # Tidak ada jalur ditemukan

# Jalankan BFS dan DFS dari Rumah (0) ke UKWMS Kalijudan (17)
bfs_path = bfs(0, 17)
dfs_path = dfs(0, 17)

# Tampilkan hasil
print("Jalur BFS (Jalur Terpendek dalam Langkah):", bfs_path)
print("Jalur DFS (Jalur dengan Pencarian Mendalam):", dfs_path)
