"""
Giải thích về Số dư bậc hai (Quadratic Residue)

1. Số dư bậc hai là gì? (Định nghĩa)
Một số `a` được gọi là số dư bậc hai modulo n nếu nó là số dư của một số chính phương nào đó khi chia cho `n`.
Định nghĩa chính thức: Cho số nguyên `a` và số nguyên dương `n`. `a` được gọi là một số dư bậc hai modulo `n` nếu tồn tại một số nguyên `x` sao cho:
x² ≡ a (mod n)
Nếu không tồn tại giá trị `x` nào như vậy, `a` được gọi là số bất dư bậc hai (quadratic non-residue).

2. Cách nó hoạt động (Ví dụ minh họa)
Ví dụ với n = 7 (một số nguyên tố).
1² ≡ 1 (mod 7)
2² ≡ 4 (mod 7)
3² ≡ 2 (mod 7)
4² ≡ 2 (mod 7)
5² ≡ 4 (mod 7)
6² ≡ 1 (mod 7)
- Các số dư bậc hai modulo 7 là: {1, 2, 4}.
- Các số bất dư bậc hai modulo 7 là: {3, 5, 6}.

3. Các khái niệm liên quan (Cách kiểm tra)
a. Ký hiệu Legendre (Legendre Symbol): (a/p)
- (a/p) = 1 nếu `a` là số dư bậc hai modulo `p`.
- (a/p) = -1 nếu `a` là số bất dư bậc hai modulo `p`.
- (a/p) = 0 nếu `a` ≡ 0 (mod p).

b. Tiêu chuẩn Euler (Euler's Criterion):
Công thức: a^((p-1)/2) ≡ (a/p) (mod p)
- Nếu a^((p-1)/2) ≡ 1 (mod p), thì `a` là số dư bậc hai.
- Nếu a^((p-1)/2) ≡ -1 (mod p), thì `a` là số bất dư bậc hai.

4. Tại sao nó quan trọng trong Mật mã học?
Nó tạo ra một "bài toán khó", làm nền tảng cho các hàm một chiều (one-way function).
- Dễ: Tính x² mod p.
- Khó: Tìm x sao cho x² ≡ a (mod p).
Ứng dụng trong các hệ mật mã như Goldwasser-Micali, giao thức chứng minh không tiết lộ kiến thức, và kiểm tra tính nguyên tố.
"""
p = 29
targets = [14, 6, 11]

# Tập các bình phương:
squares = {(a*a) % p for a in range(1, p)}
print("Quadratic residues mod", p, ":", sorted(squares))

for t in targets:
    test = pow(t, (p-1)//2, p)
    if test == 1:
        roots = [a for a in range(1, p) if (a*a) % p == t]
        print(f"{t} is a quadratic residue. Roots: {roots} (smaller = {min(roots)})")
    else:
        print(f"{t} is NOT a quadratic residue (Euler test gave {test}).")

# Quadratic Residues Problem (CryptoHack style)
# ---------------------------------------------
# Bài toán: Cho p = 29 và tập số [14, 6, 11].
# Cần xác định số nào là Quadratic Residue (QR), tức là tồn tại a sao cho:
#    a^2 ≡ x (mod p)
# Nếu tồn tại, tìm căn bậc hai modulo p của số đó.
# Nếu có 2 nghiệm (a và -a), ta chọn nghiệm nhỏ hơn.

# ---------------------------------------------
# Giải thích lý thuyết:
# - Một số x là Quadratic Residue modulo p nếu tồn tại a sao cho a^2 ≡ x (mod p).
# - Nếu không tồn tại a như vậy, thì x gọi là Quadratic Non-Residue.
# - Trong trường hợp p là số nguyên tố, khoảng một nửa số từ 1..p-1 là Quadratic Residues.
#
# Đặc điểm:
# - Nếu a là nghiệm thì (p-a) cũng là nghiệm vì (p-a)^2 ≡ a^2 (mod p).
# - Do đó nếu có nghiệm thì luôn tồn tại đúng 2 nghiệm, trừ trường hợp đặc biệt x=0.
#
# Nhiệm vụ của ta:
# - Kiểm tra từng số trong [14, 6, 11].
# - Tìm số nào là Quadratic Residue.
# - Tính nghiệm a, chọn nghiệm nhỏ hơn.