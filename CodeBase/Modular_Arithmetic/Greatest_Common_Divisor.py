# --- Nguyên tắc của Thuật toán Euclid ---
#
# Thuật toán Euclid dựa trên một nguyên tắc đơn giản nhưng mạnh mẽ:
#
#   GCD(a, b) = GCD(b, a % b)
#
# Trong đó `a % b` là số dư của phép chia `a` cho `b`.
# Chúng ta lặp lại quá trình này, thay thế số lớn hơn bằng số nhỏ hơn,
# và số nhỏ hơn bằng số dư. Quá trình dừng lại khi số dư bằng 0.
# GCD chính là số dư khác 0 cuối cùng (hoặc số chia ở bước cuối cùng).
#
# Ví dụ bằng tay: Tìm GCD(48, 18)
# 1. a = 48, b = 18.  48 % 18 = 12.  Bây giờ ta tìm GCD(18, 12).
# 2. a = 18, b = 12.  18 % 12 = 6.   Bây giờ ta tìm GCD(12, 6).
# 3. a = 12, b = 6.   12 % 6 = 0.   Bây giờ ta tìm GCD(6, 0).
# 4. Khi b = 0, thuật toán dừng lại. Kết quả chính là a ở bước này.
#    Vậy, GCD(48, 18) = 6.


# --- Cách 1: Triển khai bằng Vòng lặp (Iterative) ---
# Đây là cách triển khai phổ biến và hiệu quả nhất trong Python.
import math


def gcd_iterative(a, b):
    """
    Tính GCD của a và b bằng thuật toán Euclid (sử dụng vòng lặp while).
    """
    while b:
        # Dòng này là cốt lõi của thuật toán.
        # a mới sẽ bằng b cũ.
        # b mới sẽ bằng số dư của a cũ chia cho b cũ.
        a, b = b, a % b
    # Khi vòng lặp kết thúc, b bằng 0 và a chứa GCD.
    return a


# --- Cách 2: Triển khai bằng Đệ quy (Recursive) ---
# Cách này thể hiện rõ hơn bản chất toán học của thuật toán.
def gcd_recursive(a, b):
    """
    Tính GCD của a và b bằng thuật toán Euclid (sử dụng đệ quy).
    """
    if b == 0:
        # Điều kiện dừng của đệ quy: nếu b là 0, thì a là GCD.
        return a
    else:
        # Gọi lại chính hàm này với b và số dư của a cho b.
        return gcd_recursive(b, a % b)


# --- Cách 3: Dùng thư viện có sẵn (Khuyên dùng) ---
# Python (từ phiên bản 3.5) cung cấp sẵn hàm `math.gcd`.
# Đây là cách tốt nhất và an toàn nhất để sử dụng trong các dự án thực tế.

# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    try:
        num1 = int(input("Nhập số nguyên thứ nhất (a): "))
        num2 = int(input("Nhập số nguyên thứ hai (b): "))

        if num1 < 0 or num2 < 0:
            print("Thuật toán Euclid thường áp dụng cho số nguyên không âm.")
        else:
            # Sử dụng cách 1
            result_iter = gcd_iterative(num1, num2)
            print(f"\n[Vòng lặp]  GCD({num1}, {num2}) = {result_iter}")

            # Sử dụng cách 2
            result_recur = gcd_recursive(num1, num2)
            print(f"[Đệ quy]     GCD({num1}, {num2}) = {result_recur}")

            # Sử dụng cách 3
            result_math = math.gcd(num1, num2)
            print(f"[Thư viện]   GCD({num1}, {num2}) = {result_math}")

    except ValueError:
        print("Lỗi: Vui lòng chỉ nhập số nguyên.")
