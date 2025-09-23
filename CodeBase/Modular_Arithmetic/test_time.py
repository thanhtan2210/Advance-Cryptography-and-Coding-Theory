import time
import random

# Cách 1: dùng % trực tiếp


def mod_direct(n, m):
    return n % m

# Cách 2: modulo dần theo từng chữ số


def mod_by_digits(num_str, m):
    r = 0
    for d in num_str:
        r = (r * 10 + int(d)) % m
    return r


# --- Test với số nhỏ ---
n_small = 8146798528947
m = 17

print("=== Test số nhỏ ===")
t1 = time.time()
res1 = mod_direct(n_small, m)
t2 = time.time()
print("Trực tiếp:", res1, "Thời gian:", t2 - t1)

t1 = time.time()
res2 = mod_by_digits(str(n_small), m)
t2 = time.time()
print("Theo chữ số:", res2, "Thời gian:", t2 - t1)


# --- Test với số cực lớn (100000 chữ số) ---
big_number_str = ''.join(str(random.randint(0, 9)) for _ in range(100000))

print("\n=== Test số cực lớn (100.000 chữ số) ===")
t1 = time.time()
res3 = mod_by_digits(big_number_str, m)
t2 = time.time()
print("Theo chữ số:", res3, "Thời gian:", t2 - t1)
