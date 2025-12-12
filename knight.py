import tkinter as tk
from tkinter import messagebox, ttk


class KnightsTour:
    """Calculate a single Knight's Tour path with Warnsdorff heuristic."""

    def __init__(self, n):
        self.n = n
        self.board = [[-1 for _ in range(n)] for _ in range(n)]
        self.moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1),
        ]
        self.solution_path = []

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
            return None

        self.board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        self.solution_path = []

        start_r, start_c = self.n - 1, 0
        self.board[start_r][start_c] = 1
        path = [(start_r, start_c)]

        if self.solve_util(start_r, start_c, 2, path):
            return self.solution_path

        return None

    def solve_util(self, r, c, move_count, path):
        if move_count > self.n * self.n:
            self.solution_path = path.copy()
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
            path.append((nr, nc))
            if self.solve_util(nr, nc, move_count + 1, path):
                return True
            path.pop()
            self.board[nr][nc] = -1

        return False

    def to_chess_notation(self, r, c):
        file_char = chr(ord("a") + c)
        rank_num = self.n - r
        return f"{file_char}{rank_num}"


class KnightTourApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Player")

        self.base_canvas_size = 640
        self.current_index = -1
        self.moves = []
        self.step_lookup = {}
        self.n = 0
        self.playing = False
        self.after_id = None

        self.light_color = "#f0d9b5"
        self.dark_color = "#b58863"
        self.visited_color = "#c7e6a3"
        self.current_color = "#5b8def"
        self.line_color = "#1f7a8c"

        self.size_var = tk.StringVar(value="5")
        self.speed_var = tk.DoubleVar(value=500)
        self.info_var = tk.StringVar(
            value="Masukkan N (N = 1 atau N >= 5) lalu tekan 'Buat Rute'."
        )

        self.square_ids = []
        self.text_ids = []
        self.line_ids = []
        self.knight_piece = None
        self.knight_label = None
        self.cell_size = 60
        self.board_size = 0

        self._build_controls()
        self._build_board_canvas()

    def _build_controls(self):
        controls = ttk.Frame(self.root, padding=(14, 12))
        controls.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(controls, text="Ukuran papan (N):").grid(row=0, column=0, sticky="w")
        size_entry = ttk.Entry(controls, textvariable=self.size_var, width=7)
        size_entry.grid(row=0, column=1, sticky="w", padx=(4, 12))

        ttk.Button(controls, text="Buat Rute", command=self.generate_tour).grid(
            row=0, column=2, padx=(0, 8)
        )

        self.prev_btn = ttk.Button(
            controls, text="Prev", command=self.prev_step, state=tk.DISABLED
        )
        self.prev_btn.grid(row=0, column=3, padx=2)

        self.play_btn = ttk.Button(
            controls, text="Play", command=self.toggle_play, state=tk.DISABLED
        )
        self.play_btn.grid(row=0, column=4, padx=2)

        self.next_btn = ttk.Button(
            controls, text="Next", command=self.next_step, state=tk.DISABLED
        )
        self.next_btn.grid(row=0, column=5, padx=2)

        self.reset_btn = ttk.Button(
            controls, text="Mulai Awal", command=self.reset_to_start, state=tk.DISABLED
        )
        self.reset_btn.grid(row=0, column=6, padx=(2, 0))

        ttk.Label(controls, text="Kecepatan (ms/step):").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )
        speed_scale = ttk.Scale(
            controls, from_=1500, to=150, variable=self.speed_var, orient="horizontal"
        )
        speed_scale.grid(row=1, column=2, columnspan=5, sticky="ew", pady=(10, 0))
        controls.columnconfigure(5, weight=1)

    def _build_board_canvas(self):
        board_frame = ttk.Frame(self.root, padding=(14, 10, 14, 14))
        board_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            board_frame,
            width=self.base_canvas_size,
            height=self.base_canvas_size,
            background="#e6e6e6",
            highlightthickness=0,
        )
        self.canvas.pack()

        ttk.Label(board_frame, textvariable=self.info_var, anchor="w").pack(
            fill=tk.X, pady=(10, 0)
        )

    def generate_tour(self):
        self.stop_playback()
        try:
            n = int(self.size_var.get())
        except ValueError:
            messagebox.showerror("Input tidak valid", "N harus berupa integer.")
            return

        if n <= 0:
            messagebox.showerror("Input tidak valid", "N harus bilangan positif.")
            return

        if 1 < n < 5:
            messagebox.showwarning(
                "Tidak ada solusi",
                "Papan ukuran 2x2, 3x3, atau 4x4 secara matematis tidak memiliki solusi Knight's Tour.",
            )
            self._prepare_board(n)
            self._clear_path()
            self.render_position()
            return

        tour = KnightsTour(n)
        path = tour.solve()

        self._prepare_board(n)
        if not path:
            messagebox.showwarning(
                "Tidak ditemukan",
                "Tidak ada solusi yang ditemukan untuk ukuran ini.",
            )
            self._clear_path()
            self.render_position()
            return

        self.moves = path
        self.step_lookup = {pos: idx + 1 for idx, pos in enumerate(path)}
        self.current_index = 0
        self.info_var.set(
            f"Papan {n}x{n} siap. Play untuk animasi atau langkah manual."
        )
        self.render_position()

    def _prepare_board(self, n):
        self.n = n
        self.cell_size = max(24, int(self.base_canvas_size / max(n, 8)))
        self.board_size = self.cell_size * n
        self.canvas.config(width=self.board_size, height=self.board_size)
        self.canvas.delete("all")

        self.square_ids = []
        self.text_ids = []
        self.line_ids = []
        self.knight_piece = None
        self.knight_label = None

        for r in range(n):
            rect_row = []
            text_row = []
            for c in range(n):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = self.light_color if (r + c) % 2 == 0 else self.dark_color
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="#3b3b3b", width=1
                )
                text = self.canvas.create_text(
                    x1 + self.cell_size / 2,
                    y1 + self.cell_size / 2,
                    text="",
                    font=("Helvetica", max(10, self.cell_size // 3), "bold"),
                    fill="#1f1f1f",
                )
                rect_row.append(rect)
                text_row.append(text)
            self.square_ids.append(rect_row)
            self.text_ids.append(text_row)

    def _clear_path(self):
        self.moves = []
        self.step_lookup = {}
        self.current_index = -1
        self.playing = False
        self.after_id = None

    def toggle_play(self):
        if not self.moves:
            return
        if self.playing:
            self.stop_playback()
            return
        self.playing = True
        self.play_btn.config(text="Pause")
        self.update_controls_state()
        self._schedule_next()

    def stop_playback(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.playing = False
        self.play_btn.config(text="Play")
        self.update_controls_state()

    def _schedule_next(self):
        if not self.playing:
            return
        if self.current_index >= len(self.moves) - 1:
            self.stop_playback()
            return
        delay = max(100, int(self.speed_var.get()))
        self.after_id = self.root.after(delay, self._advance_one)

    def _advance_one(self):
        if self.current_index < len(self.moves) - 1:
            self.current_index += 1
            self.render_position()
            self._schedule_next()
        else:
            self.stop_playback()

    def next_step(self):
        if not self.moves or self.current_index >= len(self.moves) - 1:
            return
        self.stop_playback()
        self.current_index += 1
        self.render_position()

    def prev_step(self):
        if not self.moves or self.current_index <= 0:
            return
        self.stop_playback()
        self.current_index -= 1
        self.render_position()

    def reset_to_start(self):
        if not self.moves:
            return
        self.stop_playback()
        self.current_index = 0
        self.render_position()

    def render_position(self):
        if self.n == 0:
            return

        for r in range(self.n):
            for c in range(self.n):
                base_color = self.light_color if (r + c) % 2 == 0 else self.dark_color
                fill_color = base_color
                text_value = ""

                if self.moves:
                    order = self.step_lookup.get((r, c))
                    if order is not None and order <= self.current_index + 1:
                        text_value = str(order)
                        if order == self.current_index + 1:
                            fill_color = self.current_color
                        else:
                            fill_color = self.visited_color

                self.canvas.itemconfig(self.square_ids[r][c], fill=fill_color)
                self.canvas.itemconfig(self.text_ids[r][c], text=text_value)

        self._update_lines()
        self._update_knight_piece()
        self._update_info()
        self.update_controls_state()

    def _update_lines(self):
        target_count = max(0, min(self.current_index, len(self.moves) - 1))

        while len(self.line_ids) > target_count:
            self.canvas.delete(self.line_ids.pop())

        while len(self.line_ids) < target_count:
            idx = len(self.line_ids)
            start = self.moves[idx]
            end = self.moves[idx + 1]
            sx, sy = self._cell_center(start)
            ex, ey = self._cell_center(end)
            width = max(2, self.cell_size // 12)
            line = self.canvas.create_line(
                sx, sy, ex, ey, fill=self.line_color, width=width, arrow=tk.LAST
            )
            self.line_ids.append(line)

    def _update_knight_piece(self):
        if not self.moves or self.current_index < 0:
            if self.knight_piece:
                self.canvas.delete(self.knight_piece)
                self.knight_piece = None
            if self.knight_label:
                self.canvas.delete(self.knight_label)
                self.knight_label = None
            return

        x, y = self._cell_center(self.moves[self.current_index])
        padding = max(6, self.cell_size // 6)
        x1 = x - self.cell_size / 2 + padding
        y1 = y - self.cell_size / 2 + padding
        x2 = x + self.cell_size / 2 - padding
        y2 = y + self.cell_size / 2 - padding

        if not self.knight_piece:
            self.knight_piece = self.canvas.create_oval(
                x1, y1, x2, y2, fill="#2d3e5f", outline=""
            )
            self.knight_label = self.canvas.create_text(
                x,
                y,
                text="N",
                fill="white",
                font=("Helvetica", max(12, self.cell_size // 2), "bold"),
            )
        else:
            self.canvas.coords(self.knight_piece, x1, y1, x2, y2)
            self.canvas.coords(self.knight_label, x, y)

    def _cell_center(self, pos):
        r, c = pos
        x = c * self.cell_size + self.cell_size / 2
        y = r * self.cell_size + self.cell_size / 2
        return x, y

    def _update_info(self):
        if not self.moves or self.current_index < 0:
            self.info_var.set("Masukkan N (N = 1 atau N >= 5) lalu tekan 'Buat Rute'.")
            return

        step_no = self.current_index + 1
        total = len(self.moves)
        r, c = self.moves[self.current_index]
        notation = self._to_notation(r, c)
        self.info_var.set(f"Langkah {step_no}/{total} • Posisi: {notation}")

    def update_controls_state(self):
        has_moves = bool(self.moves)
        at_start = self.current_index <= 0
        at_end = self.moves and self.current_index >= len(self.moves) - 1

        self.prev_btn.config(state=tk.NORMAL if has_moves and not at_start else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if has_moves and not at_end else tk.DISABLED)
        self.reset_btn.config(state=tk.NORMAL if has_moves else tk.DISABLED)

        if not has_moves or len(self.moves) <= 1:
            self.play_btn.config(state=tk.DISABLED, text="Play")
            self.playing = False
        else:
            self.play_btn.config(state=tk.NORMAL, text="Pause" if self.playing else "Play")

    def _to_notation(self, r, c):
        file_char = chr(ord("a") + c)
        rank_num = self.n - r
        return f"{file_char}{rank_num}"


def main():
    root = tk.Tk()
    KnightTourApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
