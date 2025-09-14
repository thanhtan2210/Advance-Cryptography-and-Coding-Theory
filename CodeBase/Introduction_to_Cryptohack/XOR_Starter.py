from pwn import xor

text = b"label"
key = 13

result = xor(text, key)
print(b"crypto{" + result + b"}")
print(result)
print(result.decode())
