def all_lis(arr):
    n = len(arr)
    if n == 0:
        return []

    dp = [1] * n
    prev = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = [j]
                elif dp[j] + 1 == dp[i]:
                    prev[i].append(j)

    max_len = max(dp)

    ends = [i for i in range(n) if dp[i] == max_len]

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
        for seq in build_sequences(end):
            all_sequences.append(seq)

    unique_sequences = []
    seen = set()

    for seq in all_sequences:
        tup = tuple(seq)
        if tup not in seen:
            seen.add(tup)
            unique_sequences.append(seq)

    return max_len, unique_sequences


if __name__ == "__main__":
    try:
        n = int(input("Masukkan panjang array (N): "))
        if n <= 0:
            print("N harus positif.")
            exit()

        raw = input(f"Masukkan {n} bilangan (dipisah spasi): ")
        arr = list(map(int, raw.strip().split()))
        arr = arr[:n]

        length, sequences = all_lis(arr)

        print("\nPanjang LIS:", length)
        print("Semua kombinasi LIS:")

        for seq in sequences:
            print(" ".join(map(str, seq)))

    except ValueError:
        print("Input harus berupa integer.")
