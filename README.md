# Praktikum Teori Graf C 2025
| Name           | NRP        |
| ---            | ---        |
| Mitra Partogi | 5025241017 |
| Naufal Daffa Alfa Zain | 5025241066 |
| Riyan Fadli Amazzadin | 5025241068 | 


## The Knight's Tour 

#### Kode (dalam bahasa Python)

```py
"""
Author : Mitra Partogi
Date   : 10/12/2025
""" 

""" 
Catatan :
- program dibuat lebih fleksibel untuk menerima input N >= 8
- closed tour (kuda kembali bisa kembali ke posisi awal mungkin terjadi kalau N genap)
- defaultnya open tour dijamin ada
"""
import sys

class KnightsTour:
    def __init__(self, n):
        self.n = n
        self.board = [[-1 for _ in range(n)] for _ in range(n)]
        # mewakili gerakan kuda berbentuk L
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    def is_valid(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == -1

    def get_degree(self, r, c):
        """hitung jumlah langkah valid berikutnya dari posisi (r, c)."""
        count = 0
        for dr, dc in self.moves:
            if self.is_valid(r + dr, c + dc):
                count += 1
        return count

    def solve(self):
        # pada 2 < n < 4 kt tidak memiliki solusi
        if self.n > 1 and self.n < 5:
            print(f"Papan ukuran {self.n}x{self.n} secara matematis tidak punya solusi.")
            return False

        # asumsi kuda ditaruh di pojok kiri bawah (n-1,0)
        start_r, start_c = self.n - 1, 0 
        self.board[start_r][start_c] = 1
        
        if self.solve_util(start_r, start_c, 2):
            self.print_solution()
            return True
        else:
            print("tidak ada solusi yang ditemukan (kasus langka untuk N >= 5).")
            return False

    def solve_util(self, r, c, move_count):
        if move_count > self.n * self.n:
            return True

        # disini saya menggunakan heuristik Warnsdorff: Urutkan calon langkah berdasarkan degree terendah
        # https://arxiv.org/abs/0803.4321
        next_moves = []
        for dr, dc in self.moves:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                degree = self.get_degree(nr, nc)
                next_moves.append((degree, nr, nc))
        
        # sort non-decreasing berdasarkan degree
        next_moves.sort(key=lambda x: x[0])

        for _, nr, nc in next_moves:
            self.board[nr][nc] = move_count
            if self.solve_util(nr, nc, move_count + 1):
                return True
            self.board[nr][nc] = -1  # backtrack

        return False

    def to_chess_notation(self, r, c):
        # kolom: 0->a, 1->b, ...
        file_char = chr(ord('a') + c)
        # baris: index 0 adalah Rank N (atas), index N-1 adalah Rank 1 (bawah)
        rank_num = self.n - r
        return f"{file_char}{rank_num}"

    def print_solution(self):
        print(f"\n--- Solusi ({self.n}x{self.n}) ---")
        
        # print grid
        width = len(str(self.n * self.n))
        
        print("\nVisualisasi Board (Angka = Urutan Kunjungan):")
        # cetak header kolom (a, b, c...)
        header = "    " + " ".join([f"{chr(ord('a')+i):>{width}}" for i in range(self.n)])
        print(header)
        print("   " + "-" * (len(header)-3))

        for r in range(self.n):
            rank_label = self.n - r
            row_str = f"{rank_label:2} |"
            for c in range(self.n):
                val = self.board[r][c]
                row_str += f" {val:>{width}}"
            print(row_str)

        # cetak langkah kuda pakai notasi standar catur
        print("\n--- urutan langkah ---")
        moves_dict = {}
        for r in range(self.n):
            for c in range(self.n):
                moves_dict[self.board[r][c]] = self.to_chess_notation(r, c)
        
        moves_list = []
        for i in range(1, self.n * self.n + 1):
            moves_list.append(moves_dict[i])
        
        chunk_size = 10
        for i in range(0, len(moves_list), chunk_size):
            print(" -> ".join(moves_list[i:i+chunk_size]))

        # cek apakah closed tour / open tour
        # cari koordinat langkah terakhir (N*N)
        last_r, last_c = -1, -1
        start_r, start_c = self.n - 1, 0 

        for r in range(self.n):
            for c in range(self.n):
                if self.board[r][c] == self.n * self.n:
                    last_r, last_c = r, c
                    break
        
        # Cek apakah dari Last bisa melompat ke Start
        is_closed = False
        for dr, dc in self.moves:
            if last_r + dr == start_r and last_c + dc == start_c:
                is_closed = True
                break
        
        print(f"\n[Status Solusi]: {'CLOSED TOUR' if is_closed else 'OPEN TOUR'}")


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    
    try:
        user_input = input("input N (ukuran board NxN, N == 1 || N >= 5): ")
        n = int(user_input)
        
        if n <= 0:
            print("N harus bilangan positif.")
        else:
            tour = KnightsTour(n)
            tour.solve()
            
    except ValueError:
        print("input harus berupa integer.")
```

#### Penjelasan

Program ini mengimplementasikan solusi dari masalah **Knights Tour** menggunakan pendekatan backtracking dan heuristik **Warnsdorff's Rule**. Program ini memungkinkan pengguna untuk menemukan solusi **open tour** atau **closed tour** untuk **kuda** (knight) pada papan catur berukuran NxN, dimana N adalah input dari pengguna (dengan syarat N >= 5 atau N = 1).

### Fitur Utama:
1. **Solusi Open atau Closed Tour**: Program akan menentukan apakah solusi yang ditemukan adalah **open tour** (kuda tidak kembali ke posisi awal) atau **closed tour** (kuda kembali ke posisi awal setelah mengunjungi setiap kotak pada papan).
2. **Visualisasi Papan Catur**: Menampilkan langkah-langkah yang diambil oleh kuda dengan urutan kunjungan yang jelas, serta representasi papan catur yang menunjukkan posisi-posisi yang telah dikunjungi.
3. **Notasi Catur Standar**: Menyediakan urutan langkah dalam notasi standar catur (misalnya a1, b2, c3, dst) untuk setiap posisi yang dikunjungi oleh kuda.
4. **Validasi dan Heuristik**: Program menggunakan heuristik **Warnsdorff's Rule** untuk memilih langkah selanjutnya berdasarkan kemungkinan langkah yang paling sedikit (degree terendah), yang membantu mengurangi jumlah percabangan yang perlu dicoba.

## Persyaratan
- Python 3.x
- Tidak memerlukan pustaka tambahan.

## Penggunaan

1. **Menjalankan Program**: Setelah menjalankan skrip, pengguna diminta untuk memasukkan ukuran papan catur (N), dengan ketentuan:
   - N harus lebih besar dari 1, atau N = 1.
   - Program akan menampilkan solusi untuk masalah **Knights Tour** berdasarkan ukuran papan yang diberikan.

2. **Input**: Masukkan nilai integer untuk N yang lebih besar atau sama dengan 5, atau N = 1.

   Contoh input: nput N (ukuran board NxN, N == 1 || N >= 5): 5


3. **Output**:
- **Visualisasi Board**: Program akan mencetak papan catur NxN dengan urutan langkah yang diambil oleh kuda.
- **Urutan Langkah**: Menampilkan urutan langkah kuda dalam notasi catur standar (misalnya a1, b2, dst).
- **Status Solusi**: Menyebutkan apakah solusi yang ditemukan adalah **open tour** atau **closed tour**.

## Penjelasan Kode

### Kelas `KnightsTour`
- **Inisialisasi**:
- Papan catur `board` berukuran NxN diinisialisasi dengan nilai -1 yang menandakan kotak yang belum dikunjungi.
- Daftar `moves` berisi pasangan perubahan posisi yang memungkinkan untuk kuda (gerakan berbentuk L).

- **Metode `is_valid(r, c)`**:
- Mengecek apakah posisi `(r, c)` valid (dalam rentang papan dan belum dikunjungi).

- **Metode `get_degree(r, c)`**:
- Menghitung jumlah langkah valid yang dapat dilakukan dari posisi `(r, c)`.

- **Metode `solve()`**:
- Memulai solusi dari posisi pojok kiri bawah papan catur (baris N-1, kolom 0) dan mencoba mencari solusi menggunakan metode `solve_util()`.

- **Metode `solve_util(r, c, move_count)`**:
- Fungsi rekursif yang mencari solusi dengan backtracking.
- Menggunakan **Warnsdorff's Heuristic** untuk memilih langkah dengan degree terendah.
- Jika kuda telah mengunjungi seluruh papan, maka solusi ditemukan.

- **Metode `to_chess_notation(r, c)`**:
- Mengkonversi posisi matriks papan catur menjadi notasi standar catur (misalnya a1, b2, dst).

- **Metode `print_solution()`**:
- Menampilkan visualisasi papan catur dan urutan langkah-langkah dalam notasi catur.
- Mencetak status solusi apakah **closed tour** atau **open tour**.

### Algoritma
1. **Inisialisasi Papan**: Program menginisialisasi papan NxN dengan nilai -1 untuk menunjukkan bahwa semua kotak belum dikunjungi.
2. **Pengisian Papan**: Program memulai dari pojok kiri bawah papan dan berusaha mengisi seluruh papan dengan mengikuti langkah-langkah kuda.
3. **Backtracking**: Jika langkah yang dipilih tidak memungkinkan solusi lebih lanjut, program akan melakukan backtracking dan mencoba langkah lain.
4. **Heuristik Warnsdorff**: Heuristik ini memilih langkah yang mengarah ke kotak dengan jumlah langkah valid paling sedikit, meminimalkan kemungkinan terjebak.

### Contoh

Misalnya, untuk input `N=5`, output yang dihasilkan akan memberikan solusi langkah-langkah yang diambil kuda pada papan 5x5 beserta status apakah solusi tersebut **open tour** atau **closed tour**.

### Catatan:
- Program menjamin solusi **open tour** untuk N >= 5, namun untuk beberapa papan kecil (misalnya N = 2 atau N = 3), program tidak akan menemukan solusi.
- Jika papan terlalu kecil atau terlalu besar, hasil pencarian solusi mungkin memakan waktu lebih lama atau bahkan tidak ada solusi yang ditemukan.

## Kesimpulan
Program ini merupakan implementasi yang efisien untuk masalah **Knights Tour** dengan menggunakan algoritma backtracking dan heuristik untuk memastikan bahwa kuda dapat mengunjungi seluruh papan tanpa mengunjungi satu kotak lebih dari sekali. Program ini juga dapat menentukan apakah solusi yang ditemukan merupakan **closed tour** atau **open tour**.




## Largest Monotonically Increasing Subsequence
> file: [longest.py](https://github.com/shikajiko/C07-Praktikum-Teori-Graf/blob/main/longest.py)

### Penjelasan 

```python

def all_lis_graph(arr):
    n = len(arr)
    if n == 0:
        return 0, []
    graph = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] < arr[j]:
                graph[i].append(j)
    dp = [1] * n
    prev = [[] for _ in range(n)]
    for i in range(n):
        for j in graph[i]:
            if dp[i] + 1 > dp[j]:
                dp[j] = dp[i] + 1
                prev[j] = [i]
            elif dp[i] + 1 == dp[j]:
                prev[j].append(i)
    max_len = max(dp)
    ends = [i for i in range(n) if dp[i] == max_len]

```
Masalah ini dapat diselesaikan menggunakan DAG (Directed Acyclic Graph) dengan Dynamic Programming sebagai optimisasi. Pada awalnya, program membuat representasi graf dari angka yang dimasukkan. Ketika `arr[i]` (angka pada indeks saat ini) kurang dari `arr[j]` (angka pada indeks selanjutnya), tambahkan edge yang menghubungkan `arr[i]` ke `arr[j]`. 

Setelah mendapatkan representasi graf, program akan melakukan _graph traversal_ untuk mencari path terpanjang. Untuk meningkatkan efisiensi, program akan menyimpan ukuran path terpanjang yang mengarah ke sembarang vertex `i` dalam array `dp[i]`, sedangkan `prev[i]` adalah list semua `immediate vertex` yang menuju ke vertex `i` dan akan digunakan untuk melakukan backtracking.

```python
    def build_sequences(idx):
        if not prev[idx]:
            return [[arr[idx]]]
        sequences = []
        for p in prev[idx]:
            for seq in build_sequences(p):
                sequences.append(seq + [arr[idx]])
        return sequences

    all_sequences = []
    for end in ends:
        all_sequences.extend(build_sequences(end))

    unique_sequences = []
    seen = set()
    for seq in all_sequences:
        tup = tuple(seq)
        if tup not in seen:
            seen.add(tup)
            unique_sequences.append(seq)
    return max_len, unique_sequences
```

Terakhir, program melakukan rekonstruksi path dengan backtracking menggunakan `prev` untuk mendapatkan list naik yang terpanjang dan mengeluarkan semua baris yang valid.

### Penggunaan Program
```
python3 longest.py
```

### Input
<img width="583" height="55" alt="image" src="https://github.com/user-attachments/assets/17bd621d-a0d2-4345-aec8-60495934facb" />

### Output
<img width="583" height="139" alt="image" src="https://github.com/user-attachments/assets/5fc54635-5df8-49fb-adb0-2b6dc399b95f" />
