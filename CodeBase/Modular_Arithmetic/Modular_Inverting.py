"""modinv.py

Tính nghịch đảo modulo (modular inverse) bằng Extended Euclidean Algorithm.

Hàm chính:
 - egcd(a,b): trả về (g, x, y) sao cho a*x + b*y = g = gcd(a,b)
 - modinv(a, m): trả về d sao cho (a * d) % m == 1 ; nếu không tồn tại, ném ValueError.

Ví dụ:
 3^{-1} mod 13 = 9
 7^{-1} mod 11 = 8

Sử dụng:
    python modinv.py            # chạy ví dụ
    python modinv.py a m        # tính nghịch đảo của a modulo m
"""

import sys


def egcd(a, b):
    """Extended Euclidean Algorithm (iterative).
    Trả về (g, x, y) sao cho g = gcd(a,b) và a*x + b*y = g.
    """
    a0, b0 = abs(a), abs(b)
    old_r, r = a0, b0
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    # restore signs if a or b negative
    if a < 0:
        old_s = -old_s
    if b < 0:
        old_t = -old_t
    return old_r, old_s, old_t


def modinv(a, m):
    """Trả về nghịch đảo của a modulo m:
       tìm d sao cho a * d ≡ 1 (mod m).
       Nếu gcd(a,m) != 1 thì nghịch đảo không tồn tại (ném ValueError).
    """
    # chuẩn hóa a vào [0, m-1]
    a = a % m
    # thử dùng hàm built-in (Python 3.8+)
    try:
        inv = pow(a, -1, m)
        return inv
    except (ValueError, TypeError):
        pass
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse: gcd({a},{m}) = {g}")
    else:
        return x % m


def demo_examples():
    examples = [(3, 13), (7, 11), (2, 4)]
    for a, m in examples:
        print(f"\nTính nghịch đảo của {a} modulo {m}:")
        try:
            inv = modinv(a, m)
            print(f" => {a}^(-1) mod {m} = {inv}")
            print(f" Xác minh: ({a} * {inv}) % {m} = {(a*inv) % m}")
        except ValueError as e:
            print(f" => Lỗi: {e}")


def main(argv):
    if len(argv) == 1:
        print("Chạy ví dụ mẫu:")
        demo_examples()
    elif len(argv) == 3:
        try:
            a = int(argv[1])
            m = int(argv[2])
        except ValueError:
            print("Tham số không hợp lệ. Dùng: python modinv.py a m")
            return
        try:
            inv = modinv(a, m)
            print(f"{a}^(-1) mod {m} = {inv}")
            print(f"Xác minh: ({a} * {inv}) % {m} = {(a*inv) % m}")
        except ValueError as e:
            print(f"Lỗi: {e}")
    else:
        print("Cách dùng: python modinv.py [a m]")
        print(" Nếu không cung cấp a m, chương trình sẽ chạy ví dụ mẫu.")


if __name__ == '__main__':
    main(sys.argv)
