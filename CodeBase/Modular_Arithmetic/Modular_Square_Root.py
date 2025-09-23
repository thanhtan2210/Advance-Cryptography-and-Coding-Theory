# -*- coding: utf-8 -*-
"""
Giải pháp cho bài "Tonelli-Shanks" trên CryptoHack

Bài toán yêu cầu tìm căn bậc hai của `a` modulo `p` bằng thuật toán Tonelli-Shanks.
Đây là phương pháp tổng quát, đặc biệt khi `p` có dạng `p ≡ 1 (mod 4)`.

---
### Thuật toán Tonelli-Shanks

**Mục tiêu:** Tìm `x` sao cho `x² ≡ n (mod p)`.

1.  **Điều kiện cần:** `n` phải là một số dư bậc hai modulo `p`.
    Kiểm tra bằng Tiêu chuẩn Euler: `n^((p-1)/2) ≡ 1 (mod p)`.

2.  **Bước 1: Phân rã `p-1`**
    Viết `p - 1` dưới dạng `Q * 2^S`, trong đó `Q` là một số lẻ.

3.  **Bước 2: Tìm một số bất dư bậc hai (Non-Residue)**
    Tìm một số `z` sao cho `z^((p-1)/2) ≡ -1 (mod p)`.
    Cách đơn giản nhất là thử lần lượt các số nguyên tố nhỏ (2, 3, 5, 7,...) cho đến khi tìm được.

4.  **Bước 3: Khởi tạo các biến**
    - `M = S`
    - `c = z^Q (mod p)`
    - `t = n^Q (mod p)`
    - `R = n^((Q+1)/2) (mod p)`

5.  **Bước 4: Vòng lặp tinh chỉnh**
    Lặp cho đến khi `t ≡ 1 (mod p)`.
    - Nếu `t == 0`, nghiệm là 0.
    - Nếu `t != 1`, tìm `i` nhỏ nhất (`0 < i < M`) sao cho `t^(2^i) ≡ 1 (mod p)`.
    - Cập nhật các biến:
        - `b = c^(2^(M-i-1)) (mod p)`
        - `M = i`
        - `c = b² (mod p)`
        - `t = t * c (mod p)`
        - `R = R * b (mod p)`

6.  **Kết quả:** Khi vòng lặp kết thúc, `R` là một nghiệm. Nghiệm còn lại là `p - R`.
    Bài toán yêu cầu nộp nghiệm nhỏ hơn.

---
### Code giải
"""

def tonelli_shanks(n, p):
    # 1. Kiểm tra điều kiện
    if pow(n, (p - 1) // 2, p) != 1:
        return None # Không phải là số dư bậc hai

    # 2. Phân rã p-1 = Q * 2^S
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        S += 1
        Q //= 2
    
    if S == 1:
        # Trường hợp đơn giản p ≡ 3 (mod 4)
        return pow(n, (p + 1) // 4, p)

    # 3. Tìm số bất dư bậc hai z
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # 4. Khởi tạo
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    # 5. Vòng lặp
    while t != 1:
        if t == 0:
            return 0
        
        # Tìm i nhỏ nhất
        i = 0
        temp_t = t
        while temp_t != 1:
            temp_t = pow(temp_t, 2, p)
            i += 1
            if i == M:
                return None # Không tìm thấy nghiệm

        b = pow(c, 2**(M - i - 1), p)
        M = i
        c = pow(b, 2, p)
        t = (t * c) % p
        R = (R * b) % p
        
    return R

# Dữ liệu từ file output.txt
a = 8479994658316772151941616510097127087554541274812435112009425778595495359700244470400642403747058566807127814165396640215844192327900454116257979487432016769329970767046735091249898678088061634796559556704959846424131820416048436501387617211770124292793308079214153179977624440438616958575058361193975686620046439877308339989295604537867493683872778843921771307305602776398786978353866231661453376056771972069776398999013769588936194859344941268223184197231368887060609212875507518936172060702209557124430477137421847130682601666968691651447236917018634902407704797328509461854842432015009878011354022108661461024768
p = 30531851861994333252675935111487950694414332763909083514133769861350960895076504687261369815735742549428789138300843082086550059082835141454526618160634109969195486322015775943030060449557090064811940139431735209185996454739163555910726493597222646855506445602953689527405362207926990442391705014604777038685880527537489845359101552442292804398472642356609304810680731556542002301547846635101455995732584071355903010856718680732337369128498655255277003643669031694516851390505923416710601212618443109844041514942401969629158975457079026906304328749039997262960301209158175920051890620947063936347307238412281568760161

# Gọi hàm và tìm nghiệm
root1 = tonelli_shanks(a, p)

if root1 is not None:
    root2 = p - root1
    flag = min(root1, root2)
    print(flag)
else:
    print("Could not find the square root.")
