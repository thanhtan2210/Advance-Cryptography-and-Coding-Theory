import itertools

# --- Dữ liệu từ bài toán ---
# Đây là chuỗi mã hóa (ciphertext) dưới dạng hexa.
ciphertext_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

# Chuyển chuỗi hexa thành dạng bytes để xử lý.
ciphertext = bytes.fromhex(ciphertext_hex)

# --- Bước 1: Tìm Key bằng phương pháp "Crib Dragging" ---

# "Crib" là một đoạn bản rõ (plaintext) mà chúng ta biết hoặc đoán được.
# Trong trường hợp này, chúng ta biết FLAG có định dạng "crypto{...}".
crib = b"crypto{"

print("--- Bắt đầu tìm key ---")
print(f"Ciphertext (7 bytes đầu): {ciphertext[:7].hex()}")
print(f"Crib (đoán):             {crib.decode()}")

# Nguyên tắc: Plaintext ^ Key = Ciphertext
# Suy ra:      Key = Plaintext ^ Ciphertext
# Chúng ta sẽ XOR crib với phần đầu của ciphertext để tìm ra key.
key_part = bytes([c ^ p for c, p in zip(ciphertext, crib)])

print(f"Kết quả XOR (hex):        {key_part.hex()}")
print(f"Kết quả XOR (ascii):       {key_part.decode()}")
print("-------------------------\n")

# Kết quả "myXORke" cho thấy key có thể là "myXORkey".
# Đây là một phỏng đoán hợp lý dựa trên kinh nghiệm giải mã.
key = b"myXORkey"

# --- Bước 2: Giải mã toàn bộ Ciphertext ---

# Bây giờ chúng ta đã có key, ta cần lặp lại nó để có chiều dài bằng với ciphertext.
# Ví dụ: nếu ciphertext dài 18 bytes, key sẽ là:
# myXORkeymyXORkeymy
full_key_stream = bytes(itertools.islice(
    itertools.cycle(key), len(ciphertext)))

# Thực hiện phép XOR giữa ciphertext và chuỗi key lặp lại.
plaintext_bytes = bytes([c ^ k for c, k in zip(ciphertext, full_key_stream)])

# --- Bước 3: In kết quả ---

# Giải mã chuỗi bytes kết quả thành dạng string (utf-8) để đọc.
flag = plaintext_bytes.decode('utf-8')

print(f"Đã tìm thấy Key: {key.decode()}")
print(f"FLAG được giải mã là: {flag}")
