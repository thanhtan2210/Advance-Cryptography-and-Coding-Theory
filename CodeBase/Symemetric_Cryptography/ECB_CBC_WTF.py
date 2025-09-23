import requests

# URL gốc cho challenge
BASE_URL = "https://aes.cryptohack.org/ecbcbcwtf/"

def get_encrypted_flag():
    """
    Lấy flag đã được mã hóa từ server.
    Endpoint: /encrypt_flag/
    """
    url = BASE_URL + "encrypt_flag/"
    r = requests.get(url)
    r.raise_for_status()  # Báo lỗi nếu request thất bại
    # Ciphertext trả về ở dạng hex, cần decode thành bytes
    return bytes.fromhex(r.json()["ciphertext"])

def decrypt_ecb_oracle(ciphertext: bytes):
    """
    Gửi ciphertext đến oracle giải mã ECB.
    Endpoint: /decrypt/{ciphertext_hex}/
    """
    url = BASE_URL + f"decrypt/{ciphertext.hex()}/"
    r = requests.get(url)
    r.raise_for_status()
    # Plaintext trả về ở dạng hex, cần decode thành bytes
    return bytes.fromhex(r.json()["plaintext"])

def solve():
    """
    Thực hiện tấn công và giải mã flag.
    """
    print("[*] Getting encrypted flag from server...")
    encrypted_flag = get_encrypted_flag()
    print("[+] Successfully received ciphertext.")

    # AES có block size là 16 bytes
    block_size = 16

    # Ciphertext trả về bao gồm IV (khối đầu tiên) và các khối ciphertext (C1, C2, ...)
    iv = encrypted_flag[:block_size]
    ciphertext_blocks = [encrypted_flag[i:i+block_size] for i in range(block_size, len(encrypted_flag), block_size)]

    # --- Phân tích lỗ hổng ---
    # Server mã hóa bằng CBC mode nhưng lại giải mã bằng ECB mode.
    #
    # 1. Mã hóa CBC:
    #    C_i = E(K, P_i XOR C_{i-1})  (với C_0 = IV)
    #    Trong đó: E là hàm mã hóa, K là key, P_i là khối plaintext thứ i, C_i là khối ciphertext thứ i.
    #
    # 2. Giải mã ECB:
    #    P'_i = D(K, C_i)
    #    Trong đó: D là hàm giải mã, P'_i là khối plaintext bị lỗi (decrypted) thứ i.
    #
    # 3. Kết hợp hai quá trình:
    #    Từ (1), ta có: D(K, C_i) = P_i XOR C_{i-1}
    #    Thay vào (2), ta được: P'_i = P_i XOR C_{i-1}
    #
    # 4. Công thức tấn công:
    #    Từ kết quả trên, ta có thể tìm lại plaintext gốc P_i bằng cách:
    #    P_i = P'_i XOR C_{i-1}
    #
    #    - Đối với khối đầu tiên (i=1): P_1 = P'_1 XOR C_0 = P'_1 XOR IV
    #    - Đối với các khối sau (i>1): P_i = P'_i XOR C_{i-1}
    #
    # Tóm lại, ta có thể khôi phục plaintext gốc bằng cách lấy kết quả từ oracle giải mã ECB
    # và XOR nó với khối ciphertext liền trước đó.

    print("[*] Sending ciphertext blocks to the ECB decryption oracle...")
    # Ghép các khối C1, C2, ... để gửi đi
    ciphertext_to_decrypt = b''.join(ciphertext_blocks)
    decrypted_result = decrypt_ecb_oracle(ciphertext_to_decrypt)
    print("[+] Received garbled plaintext.")

    # Chia kết quả bị lỗi thành các khối P'_1, P'_2, ...
    decrypted_blocks = [decrypted_result[i:i+block_size] for i in range(0, len(decrypted_result), block_size)]

    # Khôi phục lại flag
    recovered_flag = b''

    print("[*] Recovering the flag from the decrypted blocks...")
    # Khôi phục khối đầu tiên: P_1 = P'_1 XOR IV
    recovered_flag += bytes(a ^ b for a, b in zip(decrypted_blocks[0], iv))

    # Khôi phục các khối còn lại: P_i = P'_i XOR C_{i-1}
    for i in range(len(ciphertext_blocks) - 1):
        recovered_flag += bytes(a ^ b for a, b in zip(decrypted_blocks[i+1], ciphertext_blocks[i]))

    # --- Xử lý Padding ---
    # Các chế độ mã hóa khối thường yêu cầu plaintext phải có độ dài là bội số của block size.
    # PKCS#7 padding là một phương pháp phổ biến: thêm N byte vào cuối, mỗi byte có giá trị N.
    # Ví dụ: nếu cần thêm 4 byte, chuỗi padding sẽ là b'\x04\x04\x04\x04'.
    # Byte cuối cùng của plaintext đã giải mã cho biết độ dài của padding.
    try:
        padding_len = recovered_flag[-1]
        if padding_len > 0 and padding_len <= block_size:
            is_padding_valid = all(p == padding_len for p in recovered_flag[-padding_len:])
            if is_padding_valid:
                recovered_flag = recovered_flag[:-padding_len]
                print("[+] Removed PKCS#7 padding.")
            else:
                print("[-] Invalid padding, not removing.")
        else:
            print("[-] No padding detected or invalid padding.")
    except IndexError:
        print("[-] Decrypted data is too short to contain padding.")


    print("\n" + "="*30)
    print("      FULLY DECRYPTED FLAG      ")
    print("="*30)
    try:
        print(f"  {recovered_flag.decode()}")
    except UnicodeDecodeError:
        print(f"  (hex): {recovered_flag.hex()}")
    print("="*30)

if __name__ == "__main__":
    solve()
