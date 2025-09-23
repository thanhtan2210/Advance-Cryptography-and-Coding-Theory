# File này chứa các hàm thực hiện các phép biến đổi ShiftRows, InvShiftRows, MixColumns và InvMixColumns
# trong thuật toán mã hóa AES.
#
# Mục tiêu của script này là giải quyết một thử thách từ cryptohack.org,
# trong đó một trạng thái (state) đã được biến đổi bằng ShiftRows và MixColumns,
# và chúng ta cần đảo ngược các phép biến đổi này để tìm ra trạng thái ban đầu (flag).

def shift_rows(s):
    # Hàm này thực hiện phép biến đổi ShiftRows trong AES.
    # Các hàng của ma trận trạng thái được dịch vòng sang trái.
    # Hàng 0 không dịch.
    # Hàng 1 dịch trái 1 byte.
    # Hàng 2 dịch trái 2 byte.
    # Hàng 3 dịch trái 3 byte.
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    # Hàm này thực hiện phép biến đổi InvShiftRows, là phép đảo ngược của ShiftRows.
    # Các hàng của ma trận trạng thái được dịch vòng sang phải.
    # Hàng 0 không dịch.
    # Hàng 1 dịch phải 1 byte.
    # Hàng 2 dịch phải 2 byte.
    # Hàng 3 dịch phải 3 byte.
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


# learned from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
def xtime(a): return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)


def mix_columns(s):
    # Hàm này thực hiện phép biến đổi MixColumns trong AES.
    # Mỗi cột của ma trận trạng thái được biến đổi bằng cách nhân với một ma trận cố định trong trường Galois GF(2^8).
    for i in range(4):
        mix_single_column(s[i])


def inv_mix_columns(s):
    # Hàm này thực hiện phép biến đổi InvMixColumns, là phép đảo ngược của MixColumns.
    # Mỗi cột của ma trận trạng thái được biến đổi bằng cách nhân với ma trận nghịch đảo của ma trận MixColumns.
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


# Trạng thái ban đầu được cung cấp trong thử thách cryptohack.
state = [
    [108, 106, 71, 86],
    [96, 62, 38, 72],
    [42, 184, 92, 209],
    [94, 79, 8, 54],
]

# Để đảo ngược các phép biến đổi, chúng ta áp dụng InvMixColumns trước, sau đó là InvShiftRows.
# Thứ tự này là quan trọng vì MixColumns được áp dụng sau ShiftRows trong quá trình mã hóa.
inv_mix_columns(state)
inv_shift_rows(state)

# Sau khi đảo ngược các phép biến đổi, chúng ta trích xuất flag từ ma trận trạng thái.
# Trạng thái được lưu trữ theo cột (column-major), vì vậy chúng ta đọc từng cột một
# và chuyển đổi các giá trị byte thành ký tự ASCII để tạo thành chuỗi flag.
flag = ""
for c in range(4):  # Duyệt qua các cột
    for r in range(4):  # Duyệt qua các hàng trong mỗi cột
        flag += chr(state[c][r])

# In ra flag đã giải mã.
print(flag)
