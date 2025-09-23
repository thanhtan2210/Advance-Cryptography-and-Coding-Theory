"""
Giải thích chi tiết quá trình giải quyết thử thách "Passwords as Keys" từ CryptoHack.

Mục tiêu của thử thách là giải mã một thông điệp đã được mã hóa. Tuy nhiên, chúng ta không có khóa giải mã trực tiếp. Thay vào đó, thử thách gợi ý rằng khóa này được tạo ra từ một mật khẩu đơn giản. Đây là một lỗ hổng bảo mật phổ biến, và chúng ta sẽ khai thác nó.

Quá trình giải quyết của tôi bao gồm các bước sau:

1. Phân tích thử thách:
    *   Thuật toán: Trang web thử thách cho biết mật mã được mã hóa bằng AES (Advanced Encryption Standard).
    *   Cách tạo khóa (Key Derivation): Khóa AES không phải là một chuỗi ngẫu nhiên, mà được tạo ra bằng cách lấy một từ trong danh sách có sẵn, sau đó băm (hash) từ đó bằng thuật toán MD5. Kết quả của hàm băm MD5 (dài 128 bit) chính là khóa AES.
    *   Tấn công: Vì không gian mật khẩu bị giới hạn trong một danh sách từ (wordlist), chúng ta có thể thực hiện một cuộc tấn công từ điển (Dictionary Attack). Ý tưởng là thử từng từ trong danh sách, tạo khóa tương ứng, và dùng nó để giải mã cho đến khi ra được kết quả có nghĩa.

2. Thu thập dữ liệu cần thiết:
    *   Lấy bản mã (Ciphertext): Tôi truy cập vào endpoint /encrypt_flag/ của thử thách để lấy về chuỗi đã được mã hóa. Đó là: c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66.
    *   Tải danh sách từ (Wordlist): Thử thách cung cấp một đường link tới một danh sách chứa hàng ngàn từ tiếng Anh thông dụng. Tôi đã tải về danh sách này.

3. Giải thích kịch bản (Script) Python:
    *   Tải danh sách từ: Script trước hết tải về danh sách các từ từ URL đã cho.
    *   Vòng lặp (Loop): Script lặp qua từng từ (mật khẩu tiềm năng) trong danh sách.
    *   Tạo khóa (Key Derivation):
        *   Với mỗi từ, nó được chuyển thành dạng bytes.
        *   Hàm băm MD5 được áp dụng cho chuỗi bytes này.
        *   Kết quả của hàm băm MD5 (một chuỗi 128-bit, hay 16-byte) chính là khóa AES được sử dụng.
    *   Giải mã (Decryption):
        *   Script sử dụng khóa vừa tạo để giải mã bản mã đã cho.
        *   Thư viện pycryptodome được dùng để thực hiện việc giải mã AES.
    *   Kiểm tra kết quả (Checking the Result):
        *   Sau khi giải mã, kết quả thu được là một chuỗi bytes (plaintext).
        *   Script cố gắng chuyển chuỗi bytes này thành dạng văn bản (string) có thể đọc được.
        *   Nó kiểm tra xem văn bản này có bắt đầu bằng "crypto{" hay không. Đây là định dạng phổ biến của các flag trong những cuộc thi CTF như Cryptohack.
    *   Tìm thấy cờ (Flag Found):
        *   Khi tìm thấy một kết quả giải mã hợp lệ (bắt đầu bằng "crypto{"), script sẽ in cờ đó ra màn hình và dừng lại.

4. Kết quả:
    *   Script đã chạy và tìm thấy mật khẩu đúng.
    *   Cờ giải được là: crypto{k3y5__r__n07__p455w0rdz?}
    *   Ý nghĩa của cờ này là một lời nhắc nhở: "keys are not passwords?" (khóa không phải là mật khẩu?), nhấn mạnh rằng việc sử dụng mật khẩu yếu, dễ đoán để làm khóa mã hóa là một lỗ hổng bảo mật nghiêm trọng.
"""
import hashlib
import requests
from Crypto.Cipher import AES

def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}

WORDLIST_URL = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
CIPHERTEXT = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"

# Download the wordlist
wordlist = requests.get(WORDLIST_URL).text.splitlines()

for password in wordlist:
    password = password.strip()
    key = hashlib.md5(password.encode()).hexdigest()
    
    decrypted_result = decrypt(CIPHERTEXT, key)
    if "plaintext" in decrypted_result:
        plaintext_bytes = bytes.fromhex(decrypted_result["plaintext"])
        try:
            plaintext = plaintext_bytes.decode('utf-8')
            if plaintext.startswith("crypto{"):
                print(f"Found flag: {plaintext}")
                break
        except UnicodeDecodeError:
            continue