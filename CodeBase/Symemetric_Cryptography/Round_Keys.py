'''
Tệp này giải thích và thực hiện thao tác "AddRoundKey" trong AES, dựa trên thử thách "Round Keys" từ CryptoHack.
Đường dẫn: https://cryptohack.org/courses/symmetric/aes3/

### Giải thích AddRoundKey

`AddRoundKey` là một trong bốn bước cơ bản trong một vòng của AES. Thao tác này thực hiện phép toán XOR theo từng byte tương ứng giữa ma trận `state` và ma trận `round_key`.

Công thức: `newState[i][j] = state[i][j] ^ round_key[i][j]`

Nhiệm vụ của chúng ta là hoàn thiện hàm `add_round_key`, sau đó sử dụng hàm `matrix2bytes` từ bài trước để chuyển ma trận kết quả thành chuỗi byte và lấy flag.
'''

state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    """Thực hiện phép XOR giữa state và round key."""
    return [[s[i][j] ^ k[i][j] for j in range(4)] for i in range(4)]


def matrix2bytes(matrix):
    """Chuyển đổi ma trận 4x4 thành một đối tượng bytes (16 byte)."""
    byte_array = []
    for row in matrix:
        for byte_val in row:
            byte_array.append(byte_val)
    return bytes(byte_array)


# 1. Thực hiện AddRoundKey để có state mới
new_state = add_round_key(state, round_key)

# 2. Chuyển đổi state mới thành bytes để lấy flag
flag_bytes = matrix2bytes(new_state)

# 3. In ra flag. Cần decode() để chuyển từ bytes sang string để hiển thị.
print(f"Flag là: {flag_bytes.decode()}")
