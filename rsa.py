#######
# third_party.py
# Acts as a Public Key Distributor (Third Party)

import socket

HOST = "localhost"
PORT_RECEIVE = 5001   # Receiver will send public key here
PORT_SEND = 5002      # Senders will request key here

print("--------------------------------------------------")
print("[THIRD PARTY SERVER STARTED]")
print("Waiting for RECEIVER to send PUBLIC KEY...")
print("--------------------------------------------------\n")

# ------------------ RECEIVE PUBLIC KEY FROM RECEIVER ------------------
recv_socket = socket.socket()
recv_socket.bind((HOST, PORT_RECEIVE))
recv_socket.listen(1)

conn, addr = recv_socket.accept()
print(f"[Third Party] Receiver connected from: {addr}")

public_key = conn.recv(4096).decode()
conn.close()

print("\n[Third Party] PUBLIC KEY RECEIVED SUCCESSFULLY!")
print("[Third Party] Received Public Key:", public_key)
print("Now storing the public key securely...\n")

# ------------------ NOW SHARE KEY WITH SENDERS ------------------
print("--------------------------------------------------")
print("[Third Party] Now READY to share PUBLIC KEY with any SENDER.")
print(f"Listening for senders on PORT {PORT_SEND} ...")
print("--------------------------------------------------\n")

send_socket = socket.socket()
send_socket.bind((HOST, PORT_SEND))
send_socket.listen(5)

while True:
    conn, addr = send_socket.accept()
    print(f"[Third Party] Sender connected: {addr}")
    print("[Third Party] Sending stored PUBLIC KEY to Sender...\n")
    
    conn.send(public_key.encode())
    conn.close()



######
#recei
# receiver.py
# Generates RSA Keys, sends PUBLIC KEY to Third Party,
# Listens for encrypted messages from Sender and decrypts them.

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

HOST = "localhost"
PORT_RECEIVE = 6000   # Receiver will listen here for encrypted messages

print("--------------------------------------------------")
print("[RECEIVER] Starting Receiver Program...")
print("--------------------------------------------------\n")

# ------------------------- KEY GENERATION -------------------------
print("[Receiver] Generating RSA Key Pair (2048 bits)...")
key = RSA.generate(2048)

private_key = key.export_key()
public_key = key.publickey().export_key()

print("\n[Receiver] RSA Key Pair Generated Successfully!")
print("--------------------------------------------------")
print("[Receiver] PUBLIC KEY (to be shared):")
print(public_key.decode())
print("--------------------------------------------------")
print("[Receiver] PRIVATE KEY (kept secret, NOT shared):")
print("(Hidden for security, but stored internally)")
print("--------------------------------------------------\n")

# ------------------------- SEND PUBLIC KEY TO THIRD PARTY -------------------------
print("[Receiver] Connecting to Third Party to SEND Public Key...")

tp = socket.socket()
tp.connect(("localhost", 5001))
tp.send(public_key)
tp.close()

print("[Receiver] Public Key Successfully Sent to Third Party!\n")

# ------------------------- LISTEN FOR ENCRYPTED MESSAGES -------------------------
print(f"[Receiver] Now Listening on port {PORT_RECEIVE} for ENCRYPTED messages...")
print("Waiting for Sender...\n")

server = socket.socket()
server.bind((HOST, PORT_RECEIVE))
server.listen(1)

while True:
    conn, addr = server.accept()
    print("--------------------------------------------------")
    print(f"[Receiver] Connection established with Sender: {addr}")
    print("[Receiver] Receiving ciphertext...")

    ciphertext = conn.recv(4096)
    conn.close()

    print("[Receiver] Ciphertext Received (Base64 Encoded):")
    print(ciphertext.decode(), "\n")

    # ------------------- DECRYPT THE MESSAGE -------------------
    print("[Receiver] Decrypting the ciphertext using PRIVATE KEY...")

    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted = cipher_rsa.decrypt(base64.b64decode(ciphertext))

    print("[Receiver] DECRYPTION SUCCESSFUL!")
    print("[Receiver] Decrypted Plaintext Message:")
    print(">>>", decrypted.decode())
    print("--------------------------------------------------\n")

######

#####
#sender
# sender.py
# Retrieves PUBLIC KEY from Third Party,
# Encrypts a user message using RSA,
# Sends ciphertext to Receiver.

import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

print("--------------------------------------------------")
print("[SENDER] Starting Sender Program...")
print("--------------------------------------------------\n")

# ---------------------- STEP 1: GET PUBLIC KEY ----------------------
print("[Sender] Connecting to Third Party to REQUEST Public Key...")

tp = socket.socket()
tp.connect(("localhost", 5002))
public_key = tp.recv(4096)
tp.close()

print("[Sender] PUBLIC KEY RECEIVED SUCCESSFULLY!")
print("--------------------------------------------------")
print("[Sender] Received Public Key:")
print(public_key.decode())
print("--------------------------------------------------\n")

# ---------------------- STEP 2: ENCRYPT MESSAGE ----------------------
msg = input("[Sender] Enter the message you want to encrypt: ").encode()

print("\n[Sender] Encrypting message using PUBLIC KEY...")
cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
ciphertext = cipher_rsa.encrypt(msg)
ciphertext_b64 = base64.b64encode(ciphertext)

print("[Sender] ENCRYPTION SUCCESSFUL!")
print("[Sender] Ciphertext (Base64 Encoded):")
print(ciphertext_b64.decode())
print("--------------------------------------------------\n")

# ---------------------- STEP 3: SEND TO RECEIVER ----------------------
print("[Sender] Connecting to Receiver to SEND encrypted message...")

receiver = socket.socket()
receiver.connect(("localhost", 6000))
receiver.send(ciphertext_b64)
receiver.close()

print("[Sender] Encrypted Message Successfully Sent to Receiver!")
print("--------------------------------------------------")
print("[Sender] Process Completed.\n")

######
