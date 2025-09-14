# This variable is likely misnamed for the challenge. It's the ciphertext.
ciphertext_hex = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

# Convert the hex string into bytes
ciphertext = bytes.fromhex(ciphertext_hex)

# The "crib" is a piece of plaintext we know or can guess.
# We know the flag format is crypto{...}
crib = b"crypto{"

# --- Crib Dragging to find the key ---
# We assume the crib is at the start of the plaintext.
# By XORing the known part of the plaintext (crib) with the corresponding
# part of the ciphertext, we can find the key.
key_candidate_part = bytes([c ^ p for c, p in zip(ciphertext, crib)])

# The pattern reveals the key is a single repeating byte.
# key_candidate_part would be b'\x10\x10\x10\x10\x10\x10\x10'
key = key_candidate_part[0] # which is 0x10

# --- Decrypt the entire message ---
# Now that we have the key, we XOR every byte of the ciphertext with it.
plaintext_bytes = bytes([byte ^ key for byte in ciphertext])

# Decode the resulting bytes into a string to read the flag.
flag = plaintext_bytes.decode('utf-8')

print("Successfully decrypted the flag:")
print(flag)