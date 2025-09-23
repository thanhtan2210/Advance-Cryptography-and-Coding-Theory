'''
Tệp này giải thích lời giải cho thử thách "Structure of AES" từ CryptoHack.
Đường dẫn: https://cryptohack.org/courses/symmetric/aes2/

### Giải thích thử thách

Thử thách này yêu cầu chúng ta thực hiện thao tác ngược lại với hàm `bytes2matrix`.

Trong AES, dữ liệu được xử lý theo các khối 16 byte. Các khối này thường được biểu diễn dưới dạng ma trận 4x4 gọi là "state" (trạng thái) để thực hiện các phép biến đổi.

Hàm `bytes2matrix` đã chuyển một chuỗi byte thành ma trận. Nhiệm vụ của chúng ta là viết hàm `matrix2bytes` để chuyển ma trận đó trở lại thành chuỗi byte ban đầu và tìm ra flag.

### Lời giải

Dựa vào ma trận được cung cấp trong thử thách, ta có thể thấy rằng các ký tự của flag được xếp vào ma trận theo thứ tự từng hàng (row-major), từ trái qua phải, từ trên xuống dưới.

Để lấy lại flag, chúng ta chỉ cần:
1. Duyệt qua từng hàng của ma trận.
2. Trong mỗi hàng, duyệt qua từng giá trị byte.
3. Chuyển mỗi giá trị byte đó thành ký tự tương ứng bằng hàm `chr()`.
4. Nối tất cả các ký tự lại để được chuỗi flag hoàn chỉnh.
'''

# Ma trận được cung cấp trong thử thách
matrix = [
    [99, 114, 121, 112],
    [116, 111, 123, 105],
    [110, 109, 97, 116],
    [114, 105, 120, 125],
]

def matrix2bytes(matrix):
    """
    Chuyển đổi ma trận 4x4 thành một chuỗi 16 byte.
    """
    text = ''
    for row in matrix:
        for byte_val in row:
            text += chr(byte_val)
    return text.encode()

# Chuyển đổi ma trận trở lại thành bytes để lấy flag
flag_bytes = matrix2bytes(matrix)

# In ra flag. Cần decode() để chuyển từ bytes sang string để hiển thị.
print(f"Flag là: {flag_bytes.decode()}")
