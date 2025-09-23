# --- I. Lý thuyết chứng minh ---

# 1. Định nghĩa cơ bản
#
# Một "số nguyên tố" là một số tự nhiên lớn hơn 1, và chỉ có đúng hai ước số dương
# là 1 và chính nó.
#
# - Ví dụ: Số 5 là số nguyên tố vì nó chỉ chia hết cho 1 và 5.
# - Ví dụ: Số 6 không phải số nguyên tố (nó là hợp số) vì nó chia hết cho 1, 2, 3, và 6.

# 2. Phương pháp kiểm tra (Phép chia thử - Trial Division)
#
# Đây là phương pháp trực tiếp và dễ hiểu nhất.
#
# - Tối ưu hóa 1: Kiểm tra đến căn bậc hai của n (√n)
#   Nếu một số `n` có một ước số `a` lớn hơn `√n`, thì nó phải có một ước số `b` nhỏ hơn `√n`.
#   Vì vậy, nếu ta không tìm thấy ước nào của `n` trong khoảng từ 2 đến `√n`,
#   thì chắc chắn cũng không có ước nào lớn hơn `√n`.
#
# - Tối ưu hóa 2: Bỏ qua các số chẵn
#   Số 2 là số nguyên tố chẵn duy nhất. Nếu một số không chia hết cho 2,
#   nó cũng không thể chia hết cho bất kỳ số chẵn nào khác.
#   Do đó, sau khi kiểm tra với số 2, ta chỉ cần kiểm tra các ước số lẻ.


# --- II. Triển khai trong Code (Python) ---

import math


def is_prime(n):
    """
    Kiểm tra một số nguyên n có phải là số nguyên tố hay không
    sử dụng phương pháp chia thử đã được tối ưu.
    """
    # --- Xử lý các trường hợp cơ bản ---
    # Số nguyên tố phải lớn hơn 1.
    if n < 2:
        return False
    # Số 2 là số nguyên tố chẵn duy nhất.
    if n == 2:
        return True
    # Tất cả các số chẵn khác (>2) không phải là số nguyên tố.
    if n % 2 == 0:
        return False

    # --- Kiểm tra các ước số lẻ ---
    # Ta chỉ cần kiểm tra các ước số lẻ từ 3 cho đến căn bậc hai của n.
    # Ta có thể nhảy 2 bước (i += 2) trong vòng lặp để chỉ xét các số lẻ (3, 5, 7, ...).
    limit = int(math.sqrt(n))
    for i in range(3, limit + 1, 2):
        # Nếu n chia hết cho i, thì n không phải là số nguyên tố.
        if n % i == 0:
            return False

    # Nếu vòng lặp kết thúc mà không tìm thấy ước nào, n là số nguyên tố.
    return True


# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    # Nhập số từ người dùng để kiểm tra
    try:
        num_input = input(
            "Nhập một số nguyên để kiểm tra (hoặc bỏ trống để xem ví dụ): ")
        if num_input:
            num = int(num_input)
            if is_prime(num):
                print(f"-> {num} LÀ một số nguyên tố.")
            else:
                print(f"-> {num} KHÔNG PHẢI là một số nguyên tố.")
        else:
            # Chạy một vài ví dụ nếu không nhập gì
            print("\n--- Chạy một vài ví dụ mặc định ---")
            test_cases = [1, 2, 3, 4, 17, 29, 57, 91, 97, 111, 113]
            for case in test_cases:
                result = "LÀ" if is_prime(case) else "KHÔNG PHẢI LÀ"
                print(f"Kiểm tra số {case}: {result} số nguyên tố.")

    except ValueError:
        print("Lỗi: Vui lòng chỉ nhập số nguyên hợp lệ.")

# Ghi chú thêm:
# Đối với các số cực lớn (ví dụ, trong mật mã RSA), phương pháp chia thử quá chậm.
# Người ta sử dụng các "phép thử xác suất" (probabilistic tests) như Fermat hay Miller-Rabin
# để kiểm tra nhanh với độ chính xác cực cao.
