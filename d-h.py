###
# third_party.py
import socket
import threading
import random

# Generate prime p and generator g (simple demo prime)
p = 509  # small prime for demonstration (use bigger prime in real life)
g = 6    # primitive root

print("=== THIRD PARTY SERVER STARTED ===")
print(f"[TP] Prime (p): {p}")
print(f"[TP] Generator (g): {g}")
print("-----------------------------------")

def handle_client(conn, addr):
    print(f"[TP] Connected with {addr}")
    data = f"{p},{g}".encode()
    conn.send(data)
    conn.close()
    print(f"[TP] Sent p & g to {addr} and closed connection.")

server = socket.socket()
server.bind(("localhost", 5001))
server.listen(5)

print("[TP] Waiting for Sender and Receiver to connect...\n")

while True:
    c, addr = server.accept()
    threading.Thread(target=handle_client, args=(c, addr)).start()

###
####
# receiver.py
import socket
import random

print("=== RECEIVER STARTED ===")

# STEP 1 — Get p and g from Third Party
tp = socket.socket()
tp.connect(("localhost", 5001))
data = tp.recv(1024).decode()
tp.close()

p, g = map(int, data.split(","))

print(f"[Receiver] Received parameters from Third Party:")
print(f"           p = {p}")
print(f"           g = {g}\n")

# STEP 2 — Generate private and public keys
private_b = random.randint(100, 999)
public_B = pow(g, private_b, p)

print(f"[Receiver] Private Key (b): {private_b}")
print(f"[Receiver] Public Key (B = g^b mod p): {public_B}\n")

# STEP 3 — Start server to receive A and send B
server = socket.socket()
server.bind(("localhost", 6000))
server.listen(1)

print("[Receiver] Waiting for Sender to connect...\n")

conn, addr = server.accept()
print(f"[Receiver] Connected with Sender {addr}")

# Receive Sender's public key A
A = int(conn.recv(1024).decode())
print(f"[Receiver] Received A = {A}")

# Send B to sender
conn.send(str(public_B).encode())
print(f"[Receiver] Sent B = {public_B}")

# STEP 4 — Derive shared key
shared_key = pow(A, private_b, p)
print(f"\n[Receiver] Shared Secret Key = {shared_key}")

# STEP 5 — Receive encrypted message
enc_msg = conn.recv(1024)
conn.close()

print(f"[Receiver] Encrypted Msg Received: {enc_msg}")

# Decrypt (simple XOR demo)
dec_msg = ''.join(chr(b ^ shared_key) for b in enc_msg)

print(f"[Receiver] Decrypted Message: {dec_msg}\n")

###

###
# sender.py
import socket
import random

print("=== SENDER STARTED ===")

# STEP 1 — Get p and g from Third Party
tp = socket.socket()
tp.connect(("localhost", 5001))
data = tp.recv(1024).decode()
tp.close()

p, g = map(int, data.split(","))

print(f"[Sender] Received parameters from Third Party:")
print(f"         p = {p}")
print(f"         g = {g}\n")

# STEP 2 — Generate private key and public key
private_a = random.randint(100, 999)
public_A = pow(g, private_a, p)

print(f"[Sender] Private Key (a): {private_a}")
print(f"[Sender] Public Key (A = g^a mod p): {public_A}\n")

# STEP 3 — Connect to receiver and exchange keys
receiver = socket.socket()
receiver.connect(("localhost", 6000))

# Send A
receiver.send(str(public_A).encode())
print(f"[Sender] Sent A = {public_A}")

# Receive B
B = int(receiver.recv(1024).decode())
print(f"[Sender] Received B = {B}")

# STEP 4 — Compute shared secret key
shared_key = pow(B, private_a, p)
print(f"\n[Sender] Shared Secret Key = {shared_key}")

# STEP 5 — Encrypt message
msg = input("\nEnter message to send: ")
enc = bytes([ord(c) ^ shared_key for c in msg])

print(f"[Sender] Encrypted Message: {enc}")

receiver.send(enc)
receiver.close()

print("[Sender] Encrypted data sent to Receiver.\n")

###