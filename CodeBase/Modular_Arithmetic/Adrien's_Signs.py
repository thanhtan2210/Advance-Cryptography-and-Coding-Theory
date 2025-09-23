"""
Giải pháp cho bài "Adrien's Signs" trên CryptoHack

Lỗ hổng của hệ mật mã này nằm ở việc có thể phân biệt được giá trị mã hóa cho bit '1' và bit '0'
dựa trên tính chất số dư bậc hai của chúng.

### Phân tích

1.  **Logic mã hóa:**
    - Bit '1': mã hóa thành `n = a^e (mod p)`
    - Bit '0': mã hóa thành `-n (mod p)`

2.  **Tính chất của p:**
    `p = 1007621497415251`, ta có `p ≡ 3 (mod 4)`.
    Theo tính chất của Ký hiệu Legendre, điều này có nghĩa là `(-1/p) = -1`.
    Nói cách khác, -1 là một số BẤT DƯ bậc hai modulo p.

3.  **Tính chất của a:**
    `a = 288260533169915`.
    Nếu ta tính `pow(a, (p-1)//2, p)`, kết quả sẽ là 1. Điều này chứng tỏ `a` là một SỐ DƯ bậc hai.

4.  **Suy luận:**
    - Vì `a` là số dư bậc hai, `n = a^e` cũng sẽ luôn là một số dư bậc hai. `(n/p) = 1`.
    - Giá trị mã hóa cho bit '0' là `-n`. Ký hiệu Legendre của nó là `(-n/p) = (-1/p) * (n/p) = -1 * 1 = -1`.
    - Do đó, `-n` luôn là một số bất dư bậc hai.

### Kết luận

- Các số trong bản mã là SỐ DƯ BẬC HAI tương ứng với bit '1'.
- Các số trong bản mã là SỐ BẤT DƯ BẬC HAI tương ứng với bit '0'.

Ta chỉ cần kiểm tra tính chất này cho từng số trong bản mã để khôi phục lại flag.
"""

# Dữ liệu từ bài toán
a = 288260533169915
p = 1007621497415251


def solve():
    # Đọc file chứa bản mã
    try:
        with open("D:/Bon Bon/Advance Cryptography and Coding Theory/Advance-Cryptography-and-Coding-Theory/CodeBase/Modular_Arithmetic/Adrien's_SIgns.txt", "r") as f:
            ciphertext = eval(f.read())
    except FileNotFoundError:
        # This will print to stderr, which is fine.
        import sys
        print("Error: Could not find Adrien's_SIgns.txt", file=sys.stderr)
        return

    binary_flag = ""
    half_p = (p - 1) // 2

    for c in ciphertext:
        legendre_symbol = pow(c, half_p, p)
        if legendre_symbol == 1:
            binary_flag += '1'
        elif legendre_symbol == p - 1:
            binary_flag += '0'

    # Chuyển chuỗi nhị phân về ASCII
    flag = ""
    for i in range(0, len(binary_flag), 8):
        byte_str = binary_flag[i:i+8]
        if len(byte_str) == 8:
            flag += chr(int(byte_str, 2))

    print(f"FLAG: {flag}")


if __name__ == "__main__":
    solve()


#  FLAG: crypto{p4tterns_1n_re5idu3s}
