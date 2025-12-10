import sys

class KnightsTour:
    def __init__(self, n):
        self.n = n
        self.board = [[-1 for _ in range(n)] for _ in range(n)]
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    def is_valid(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == -1

    def get_degree(self, r, c):
        count = 0
        for dr, dc in self.moves:
            if self.is_valid(r + dr, c + dc):
                count += 1
        return count

    def solve(self):
        if self.n > 1 and self.n < 5:
            print(f"Papan ukuran {self.n}x{self.n} secara matematis tidak punya solusi.")
            return False

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

        next_moves = []
        for dr, dc in self.moves:
            nr, nc = r + dr, c + dc
            if self.is_valid(nr, nc):
                degree = self.get_degree(nr, nc)
                next_moves.append((degree, nr, nc))
        
        next_moves.sort(key=lambda x: x[0])

        for _, nr, nc in next_moves:
            self.board[nr][nc] = move_count
            if self.solve_util(nr, nc, move_count + 1):
                return True
            self.board[nr][nc] = -1

        return False

    def to_chess_notation(self, r, c):
        file_char = chr(ord('a') + c)
        rank_num = self.n - r
        return f"{file_char}{rank_num}"

    def print_solution(self):
        print(f"\n--- Solusi ({self.n}x{self.n}) ---")
        
        width = len(str(self.n * self.n))
        
        print("\nVisualisasi Board (Angka = Urutan Kunjungan):")
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
