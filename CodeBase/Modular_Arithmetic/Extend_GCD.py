# --- Khái niệm: Thuật toán Euclid Mở rộng là gì? ---
#
# Đây là một phiên bản nâng cao của thuật toán Euclid.
# Trong khi thuật toán Euclid thông thường chỉ tìm Ước số chung lớn nhất (GCD) của hai số a và b,
# thuật toán mở rộng còn tìm được hai số nguyên x và y sao cho chúng thỏa mãn
# phương trình đặc biệt sau, gọi là "Đẳng thức Bézout":
#
#   a*x + b*y = gcd(a, b)
#

# --- Ứng dụng: Tại sao nó quan trọng? ---
#
# Ứng dụng quan trọng nhất trong mật mã học là để tìm "Nghịch đảo modular".
#
# Nghịch đảo của a (mod m) là một số x sao cho: a * x ≡ 1 (mod m).
# Điều này tương đương với việc giải phương trình: a*x + m*y = 1.
#
# Ta chỉ có thể tìm được nghịch đảo khi và chỉ khi gcd(a, m) = 1.
# Thuật toán Euclid mở rộng giúp chúng ta tìm ra x một cách hiệu quả.


# --- Logic: Thuật toán hoạt động như thế nào? ---
#
# Thuật toán hoạt động bằng cách truy ngược lại các bước của thuật toán Euclid.
# Nó có bản chất đệ quy.
#
# 1. Trường hợp cơ sở (Base Case):
#    Nếu b = 0, ta có gcd(a, 0) = a.
#    Phương trình trở thành: a*x + 0*y = a.
#    Một nghiệm rõ ràng là x = 1, y = 0.
#    Vì vậy, hàm trả về (a, 1, 0).
#
# 2. Bước đệ quy (Recursive Step):
#    Ta biết rằng gcd(a, b) = gcd(b, a % b).
#    Ta gọi đệ quy `extended_gcd(b, a % b)` để nhận về một tuple (gcd, x', y').
#    Tuple này cho ta biết: b*x' + (a % b)*y' = gcd
#
#    Ta cần biến đổi phương trình trên để nó có dạng a*x + b*y = gcd.
#    Biết rằng: a % b = a - (a // b) * b
#
#    Thay thế vào, ta có:
#    b*x' + (a - (a // b) * b)*y' = gcd
#
#    Sắp xếp lại các số hạng để nhóm a và b:
#    b*x' + a*y' - (a // b)*b*y' = gcd
#    a*y' + b*(x' - (a // b)*y') = gcd
#
#    So sánh phương trình này với phương trình gốc a*x + b*y = gcd, ta có thể thấy:
#    x = y'
#    y = x' - (a // b) * y'
#
#    Đây chính là công thức để cập nhật x và y ở mỗi bước đệ quy.


# --- Triển khai trong Python ---
def extended_gcd(a, b):
    """
    Hàm này triển khai Thuật toán Euclid Mở rộng.

    Đầu vào:
        a, b: hai số nguyên

    Đầu ra:
        Một tuple (gcd, x, y) sao cho a*x + b*y = gcd(a, b).
    """
    # Trường hợp cơ sở của đệ quy
    if b == 0:
        return (a, 1, 0)
    else:
        # Bước đệ quy: gọi hàm cho b và a % b
        gcd, x_prime, y_prime = extended_gcd(b, a % b)

        # Cập nhật x và y dựa trên kết quả của bước đệ quy (x', y')
        # theo công thức đã chứng minh ở trên.
        x = y_prime
        y = x_prime - (a // b) * y_prime

        return (gcd, x, y)


# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    # Ví dụ 1: Tìm gcd, x, y cho hai số cụ thể
    a1, b1 = 55, 80
    gcd1, x1, y1 = extended_gcd(a1, b1)

    print(f"--- Ví dụ 1: Tìm x, y cho a={a1}, b={b1} ---")
    print(f"GCD({a1}, {b1}) = {gcd1}")
    print(f"x = {x1}")
    print(f"y = {y1}")
    print("Kiểm tra đẳng thức Bézout:")
    print(f"{a1} * ({x1}) + {b1} * ({y1}) = {a1*x1 + b1*y1}")
    print(f"Kết quả có bằng GCD không? -> {a1*x1 + b1*y1 == gcd1})")
    # Ví dụ 2: Ứng dụng tìm nghịch đảo modular
    # Tìm nghịch đảo của 17 modulo 3120
    a2, m2 = 17, 3120
    gcd2, x2, y2 = extended_gcd(a2, m2)

    print(f"--- Ví dụ 2: Tìm nghịch đảo của {a2} (mod {m2}) ---")
    if (gcd2 != 1):
        print(f"{a2} không có nghịch đảo modulo {m2} vì GCD của chúng không phải là 1.")
    else:
        # Giá trị x có thể là số âm.
        # Ta cần dùng phép toán modulo để đảm bảo kết quả nằm trong khoảng [0, m-1].
        inverse = x2 % m2
        print(f"Nghịch đảo của {a2} (mod {m2}) là: {inverse}")
        print("Kiểm tra lại:")
        print(f"({a2} * {inverse}) % {m2} = {(a2 * inverse) % m2}")
