import requests
import time

# --- Phần giải thích --- #
# Lỗ hổng của chế độ ECB (Electronic Codebook):
# Chế độ ECB mã hóa mỗi khối (block) dữ liệu 16-byte một cách độc lập với cùng một khóa.
# Điều này có nghĩa là: NẾU Plaintext_Block_A == Plaintext_Block_B THÌ Ciphertext_Block_A == Ciphertext_Block_B.
# Đây là một điểm yếu chí mạng, cho phép chúng ta thực hiện cuộc tấn công "byte-at-a-time".
#
# Kịch bản tấn công:
# Oracle mã hóa theo công thức: AES_ECB(KEY, YOUR_INPUT + SECRET_FLAG)
# Mục tiêu của chúng ta là tìm ra SECRET_FLAG.
#
# Ý tưởng tấn công:
# Chúng ta có thể đoán từng byte của SECRET_FLAG bằng cách sắp xếp cho byte đó nằm ở cuối một khối plaintext mà chúng ta kiểm soát.
#
# Ví dụ tìm byte đầu tiên (S_0) của flag:
# 1. Gửi một payload có độ dài (block_size - 1), ví dụ: "AAAAAAAAAAAAAAA" (15 chữ A).
#    Oracle sẽ mã hóa: "AAAAAAAAAAAAAAA" + S_0 + S_1 + ...
#    Khối plaintext đầu tiên sẽ là: "AAAAAAAAAAAAAAA" + S_0
#    Ta lấy ciphertext của khối này làm "mục tiêu" (target_block).
#
# 2. Bây giờ, ta thử tất cả các khả năng cho S_0 (từ 0 đến 255).
#    Với mỗi byte `b` khả thi, ta gửi payload: "AAAAAAAAAAAAAAA" + `b`
#    Oracle sẽ mã hóa payload này. Khối plaintext đầu tiên chính là "AAAAAAAAAAAAAAA" + `b`.
#    Ta lấy ciphertext của khối này và so sánh với `target_block` ở trên.
#
# 3. Nếu hai ciphertext block khớp nhau, ta đã tìm thấy byte S_0 chính là `b`.
#
# Tương tự, để tìm byte thứ hai (S_1), ta sẽ gửi payload "AAAAAAAAAAAAAA" (14 chữ A) để có target_block,
# và gửi "AAAAAAAAAAAAAA" + S_0_đã_biết + `b` để thử các khả năng cho S_1.
# Quá trình này được lặp lại cho đến khi tìm thấy toàn bộ flag.

BASE_URL = "https://aes.cryptohack.org/ecb_oracle/encrypt/{}"
# Nếu server báo lỗi rate-limit, hãy tăng giá trị này (ví dụ: 0.1)
SLEEP_BETWEEN_REQUESTS = 0.1

def query_oracle(payload: bytes) -> bytes:
    """Gửi payload đến oracle và nhận lại ciphertext."""
    hex_payload = payload.hex()
    if not hex_payload:
        # API không chấp nhận payload rỗng, gửi 1 byte null để thay thế
        hex_payload = "00"

    url = BASE_URL.format(hex_payload)
    try:
        r = requests.get(url)
        r.raise_for_status()
        response_json = r.json()
        if "ciphertext" in response_json:
            if SLEEP_BETWEEN_REQUESTS > 0:
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            return bytes.fromhex(response_json["ciphertext"])
        else:
            raise ValueError(f"API response does not contain 'ciphertext': {response_json}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request to server failed: {e}")
        raise
    except ValueError as e:
        print(f"[ERROR] Failed to parse JSON response: {e}")
        raise

def detect_block_size(max_probe: int = 48) -> int:
    """Tự động phát hiện block size bằng cách gửi payload tăng dần."""
    initial_len = len(query_oracle(b''))
    for i in range(1, max_probe + 1):
        payload = b'A' * i
        new_len = len(query_oracle(payload))
        if new_len > initial_len:
            return new_len - initial_len
    raise RuntimeError("Could not auto-detect block size.")

def recover_flag(block_size: int, max_len: int = 128) -> bytes:
    """Thực hiện tấn công byte-at-a-time để khôi phục flag."""
    recovered = b''
    for i in range(max_len):
        # 1. Chuẩn bị payload để lấy block mục tiêu (target_block)
        padding_len = (block_size - 1 - len(recovered)) % block_size
        padding = b'A' * padding_len

        target_block_index = len(recovered) // block_size

        ciphertext1 = query_oracle(padding)
        target_block = ciphertext1[target_block_index * block_size : (target_block_index + 1) * block_size]

        # 2. Thử tất cả các byte để tìm byte khớp
        known_part = padding + recovered
        prefix = known_part[-(block_size - 1):]

        found_byte = None
        for byte_guess in range(256):
            test_payload = prefix + bytes([byte_guess])
            ciphertext2 = query_oracle(test_payload)
            test_block = ciphertext2[:block_size]

            if test_block == target_block:
                found_byte = bytes([byte_guess])
                break

        if found_byte:
            recovered += found_byte
            print(f"[+] Found: {recovered.decode(errors='ignore')}", end='\r')
            if found_byte == b'}':
                print("\n[*] Looks like we found the full flag!")
                return recovered
        else:
            print("\n[*] No more bytes found. Stopping.")
            return recovered

    return recovered

if __name__ == '__main__':
    try:
        print("[*] Starting ECB oracle attack...")
        print("[*] Auto-detecting block size...")
        bs = detect_block_size()
        print(f"[+] Detected block size = {bs} bytes")

        flag = recover_flag(bs)

        print("\n" + "="*30)
        print("      FINAL FLAG      ")
        print("="*30)
        print(f"  {flag.decode(errors='ignore')}")
        print("="*30)

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")