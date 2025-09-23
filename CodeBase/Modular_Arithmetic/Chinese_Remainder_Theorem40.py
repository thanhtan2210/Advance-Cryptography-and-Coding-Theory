# -*- coding: utf-8 -*-
"""
Giải pháp cho bài "Chinese Remainder Theorem" trên CryptoHack

Định lý số dư Trung Hoa (CRT) cung cấp một phương pháp để tìm một số nguyên `x`
thỏa mãn đồng thời nhiều phương trình đồng dư, với điều kiện các mô-đun (moduli)
là nguyên tố cùng nhau.

Bài toán cho hệ phương trình:
x ≡ 2 (mod 5)
x ≡ 3 (mod 11)
x ≡ 5 (mod 17)

---
### Thuật toán giải (Phương pháp xây dựng)

Cho hệ phương trình:
x ≡ a_1 (mod n_1)
x ≡ a_2 (mod n_2)
...
x ≡ a_k (mod n_k)

1.  **Tính N:**
    N là tích của tất cả các mô-đun: N = n_1 * n_2 * ... * n_k.

2.  **Với mỗi phương trình i:**
    a. Tính `N_i = N / n_i`.
    b. Tìm nghịch đảo modular của `N_i` theo `n_i`. Gọi là `y_i`.
       `y_i` là số thỏa mãn `(N_i * y_i) ≡ 1 (mod n_i)`.
       Trong Python, ta có thể tính dễ dàng bằng `y_i = pow(N_i, -1, n_i)`.

3.  **Tính x:**
    Nghiệm `x` được tìm bằng công thức:
    x = (a_1*N_1*y_1 + a_2*N_2*y_2 + ... + a_k*N_k*y_k) mod N

---
### Áp dụng vào bài toán

- a = [2, 3, 5]
- n = [5, 11, 17]

1.  N = 5 * 11 * 17 = 935

2.  Tính toán cho từng phương trình:
    - i=1: a=2, n=5
      N_1 = 935 / 5 = 187
      y_1 = pow(187, -1, 5) = pow(2, -1, 5) = 3
    - i=2: a=3, n=11
      N_2 = 935 / 11 = 85
      y_2 = pow(85, -1, 11) = pow(8, -1, 11) = 7
    - i=3: a=5, n=17
      N_3 = 935 / 17 = 55
      y_3 = pow(55, -1, 17) = pow(4, -1, 17) = 13

3.  Tổng hợp kết quả:
    x = (2*187*3 + 3*85*7 + 5*55*13) mod 935
    x = (1122 + 1785 + 3575) mod 935
    x = 6482 mod 935
    x = 872

---
### Code giải
"""

import functools
import operator

# Dữ liệu từ bài toán
congruences = [
    (2, 5),
    (3, 11),
    (5, 17)
]


def solve_crt(congruences):
    """
    Giải hệ phương trình đồng dư bằng Định lý số dư Trung Hoa.
    `congruences` là một list các cặp (a_i, n_i).
    """
    # Tách a và n từ list
    a_list = [c[0] for c in congruences]
    n_list = [c[1] for c in congruences]

    # Bước 1: Tính N
    N = functools.reduce(operator.mul, n_list)

    # Bước 2 & 3: Tính tổng
    total = 0
    for a_i, n_i in congruences:
        N_i = N // n_i
        y_i = pow(N_i, -1, n_i)
        total += a_i * N_i * y_i

    # Kết quả cuối cùng
    return total % N


# Giải và in kết quả
x = solve_crt(congruences)
print(x)
