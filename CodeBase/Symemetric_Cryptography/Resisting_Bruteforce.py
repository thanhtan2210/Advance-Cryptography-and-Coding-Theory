'''
Tệp này giải thích lời giải cho thử thách "Resisting Bruteforce" từ CryptoHack.
Đường dẫn: https://cryptohack.org/courses/symmetric/aes1/

### Giải thích thử thách

Thử thách này giới thiệu về khả năng chống lại tấn công brute-force (vét cạn) của mật mã khối, cụ thể là AES.

1.  **Không gian khóa (Keyspace)**: Sức mạnh của một thuật toán mã hóa chống lại tấn công brute-force nằm ở kích thước không gian khóa của nó. Với khóa 128-bit của AES, không gian khóa là 2^128. Một cuộc tấn công brute-force sẽ đòi hỏi phải thử tất cả 2^128 trường hợp, một con số khổng lồ và không khả thi với công nghệ hiện tại.

2.  **Tấn công trên lý thuyết**: Tuy nhiên, thử thách đề cập đến một cuộc tấn công trên lý thuyết có hiệu quả hơn brute-force một chút. Cuộc tấn công này làm giảm độ an toàn của AES-128 từ 2^128 xuống còn 2^126.1.

### Lời giải

Cuộc tấn công được nói đến là **tấn công biclique (biclique attack)**. Đây là cuộc tấn công hiệu quả nhất được biết đến chống lại AES.

Mặc dù có tồn tại, cuộc tấn công này vẫn chỉ mang tính lý thuyết và không thể thực hiện trong thực tế. Do đó, AES-128 vẫn được coi là cực kỳ an toàn cho các ứng dụng thông thường.

Flag cho thử thách này chính là tên của cuộc tấn công đó.
'''

# Flag chính xác cho thử thách
flag = "crypto{biclique}"

print(f"Flag là: {flag}")
