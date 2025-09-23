# --- Phân tích Thử thách ---
#
# 1. Bối cảnh:
#    - Thử thách giới thiệu về "Modes of Operation" (Các chế độ hoạt động) của mật mã khối.
#    - Các thuật toán như AES chỉ mã hóa được các khối dữ liệu có kích thước cố định (16 bytes).
#    - Các chế độ hoạt động cho phép mã hóa các thông điệp dài hơn một khối.
#
# 2. API được cung cấp:
#    - Thử thách cung cấp một giao diện tương tác tại `https://aes.cryptohack.org/block_cipher_starter/`
#    - Giao diện này có 2 endpoint chính:
#      a) /encrypt_flag/
#         - Khi được gọi, endpoint này sẽ mã hóa một FLAG bí mật bằng thuật toán AES, chế độ ECB với một KEY bí mật.
#         - Kết quả trả về là một chuỗi ciphertext dưới dạng hex.
#         - Source code phía server:
#           cipher = AES.new(KEY, AES.MODE_ECB)
#           encrypted = cipher.encrypt(FLAG.encode())
#
#      b) /decrypt/<ciphertext>/
#         - Endpoint này nhận một chuỗi ciphertext (dạng hex) làm tham số.
#         - Nó sẽ giải mã chuỗi này bằng cùng thuật toán AES, chế độ ECB và cùng KEY bí mật ở trên.
#         - Kết quả trả về là chuỗi plaintext dưới dạng hex.
#         - Source code phía server:
#           cipher = AES.new(KEY, AES.MODE_ECB)
#           decrypted = cipher.decrypt(ciphertext)
#
# --- Lỗ hổng (The Vulnerability) ---
#
# Lỗ hổng chính nằm ở việc sử dụng cùng một khóa (KEY) và cùng một chế độ mã hóa (AES-ECB) cho cả hai chức năng:
# - Mã hóa flag bí mật.
# - Giải mã một chuỗi ciphertext bất kỳ do người dùng cung cấp.
#
# AES là một "keyed permutation", nghĩa là với một khóa K, nó tạo ra một ánh xạ song ánh (một-đối-một và thuận nghịch) giữa plaintext và ciphertext.
#   - Encrypt(Plaintext, Key) = Ciphertext
#   - Decrypt(Ciphertext, Key) = Plaintext
#
# Do đó, nếu chúng ta có thể lấy được `Ciphertext` của `FLAG`, chúng ta có thể gửi chính `Ciphertext` đó đến hàm giải mã để lấy lại `FLAG` ban đầu.
#
# --- Kế hoạch Tấn công ---
#
# 1. **Bước 1: Lấy Ciphertext của Flag**
#    - Gửi một yêu cầu GET đến endpoint: `https://aes.cryptohack.org/block_cipher_starter/encrypt_flag/`
#    - Server sẽ trả về một JSON object chứa ciphertext của flag.
#
# 2. **Bước 2: Giải mã Ciphertext**
#    - Lấy giá trị ciphertext từ Bước 1.
#    - Gửi một yêu cầu GET đến endpoint: `https://aes.cryptohack.org/block_cipher_starter/decrypt/<ciphertext>/`
#      (thay `<ciphertext>` bằng giá trị đã lấy).
#    - Server sẽ trả về một JSON object chứa plaintext (chính là flag) dưới dạng hex.
#
# 3. **Bước 3: Đọc Flag**
#    - Chuyển đổi chuỗi hex nhận được từ Bước 2 sang định dạng ASCII để đọc flag.
#
# --- Thực thi và Kết quả ---

# Bước 1: Gọi API để mã hóa flag
# Yêu cầu: GET https://aes.cryptohack.org/block_cipher_starter/encrypt_flag/
# Kết quả trả về (ví dụ): {"ciphertext": "c11949a4a2ecf929dfce48b39daedd9e6d90c67d2f550b79259bdda835348a48"}
encrypted_flag_hex = "c11949a4a2ecf929dfce48b39daedd9e6d90c67d2f550b79259bdda835348a48"

# Bước 2: Gửi ciphertext vừa nhận được để giải mã
# Yêu cầu: GET https://aes.cryptohack.org/block_cipher_starter/decrypt/c11949a4a2ecf929dfce48b39daedd9e6d90c67d2f550b79259bdda835348a48/
# Kết quả trả về (ví dụ): {"plaintext": "63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d"}
decrypted_flag_hex = "63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d"

# Bước 3: Chuyển đổi hex sang ASCII
try:
    flag = bytes.fromhex(decrypted_flag_hex).decode('utf-8')
except (ValueError, UnicodeDecodeError) as e:
    flag = f"Error decoding flag: {e}"


# --- Kết luận ---
#
# Flag cuối cùng là:
print(f"The flag is: {flag}")

# FLAG: crypto{bl0ck_c1ph3r5_4r3_f457_!}
