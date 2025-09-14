# KEY1 = a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
# KEY2 ^ KEY1 = 37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
# KEY2 ^ KEY3 = c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
# FLAG ^ KEY1 ^ KEY3 ^ KEY2 = 04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf
# hex=>bytes

# Values from the file
key1_hex = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
# value_3 = KEY2 ^ KEY3
value_3_hex = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
# value_4 = FLAG ^ KEY1 ^ KEY3 ^ KEY2
value_4_hex = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

# Convert hex strings to integers
key1 = int(key1_hex, 16)
value_3 = int(value_3_hex, 16)
value_4 = int(value_4_hex, 16)

# As derived: FLAG = value_4 ^ key1 ^ value_3
flag_int = value_4 ^ key1 ^ value_3

# Convert the resulting integer to bytes.
flag_bytes = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, 'big')

# Decode the bytes into a human-readable string
flag_str = flag_bytes.decode('utf-8')

print(f"FLAG là: {flag_str}")
