
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        gcd, x_prime, y_prime = extended_gcd(b, a % b)
        x = y_prime
        y = x_prime - (a // b) * y_prime
        return (gcd, x, y)

p = 26513
q = 32321

gcd, u, v = extended_gcd(p, q)

# The flag format for CryptoHack is crypto{u,v}
print(f"crypto{{{u},{v}}}")
