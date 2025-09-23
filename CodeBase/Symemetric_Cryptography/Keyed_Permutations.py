'''
Tệp này giải thích lời giải cho thử thách "Keyed Permutations" từ CryptoHack.
Đường dẫn: https://cryptohack.org/courses/symmetric/aes0/

Giải thích thử thách:

Đây là một thử thách về khái niệm, không phải là một bài toán lập trình. Thử thách yêu cầu thuật ngữ toán học mô tả thuộc tính của một hoán vị có khóa (keyed permutation) được sử dụng trong các mật mã khối như AES.

Một mật mã khối phải có tính thuận nghịch, nghĩa là với mỗi đầu vào phải có một đầu ra duy nhất, và ngược lại, với mỗi đầu ra cũng phải có một đầu vào duy nhất. Sự tương ứng một-đối-một này là thuộc tính chính.

Dữ liệu được cung cấp (các hoán vị, bản rõ, bản mã) chỉ là "mồi nhử" (red herring), được thiết kế để đánh lừa bạn vào một bài toán lập trình phức tạp không có lời giải với các con số đã cho.

Lời giải:

Thuật ngữ toán học cho sự tương ứng một-đối-một (một hàm vừa là đơn ánh, vừa là toàn ánh) là "song ánh" (bijection).

Do đó, flag chính là từ "bijection" được đặt trong định dạng của flag.
'''

# Flag chính xác cho thử thách
flag = "crypto{bijection}"

print(f"Flag là: {flag}")
