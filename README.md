# 🔐 Encrypted Remote Keylogger

A Python-based remote keylogger system that securely logs keystrokes on a client machine and transmits them to a receiver over a TCP connection using Fernet symmetric encryption.

> ⚠️ **For educational and ethical use only. Do not deploy or use without proper authorization.**

---

## 📌 Features

- Real-time keystroke logging
- Fernet AES encryption for secure transmission
- Remote kill switch support
- Local logging of plaintext and encrypted data
- Simple socket-based client-server communication

---

## 🧰 Technologies Used

- Python 3
- `pynput` – Keyboard event listener
- `cryptography.fernet` – For secure encryption/decryption
- `socket` – TCP networking (standard library)
- `threading`, `datetime`, `os` – Standard Python modules

---

## 🚀 Setup Instructions

### 1. Clone the Repository
`git clone https://github.com/your-username/encrypted-keylogger.git
cd encrypted-keylogger`

### 2. Install Dependencies
`pip install -r requirements.txt`

### 3. Configuration
- Update SERVER_IP and PORT in both scripts (sender.py and receiver.py) to match your environment.
- Ensure both sender and receiver share the same Fernet KEY.

--

## 🧠 Usage

### 📤 Sender (Keylogger)
`python keylogger_sender_encrypted.py`
- Starts capturing keystrokes.
- Sends encrypted data to the receiver.
- Can be stopped remotely via kill command or locally using the Escape key.

### 📥 Receiver (Server)
`python receiver_encrypted.py`
- Listens for incoming encrypted data.
- Decrypts and logs data in real-time.
- Enter "kill" in the console to remotely stop the sender *OR* Enter "Lctrl+Lshift+q" on the sender side to kill the keylogger locally.

--

## 📄 Log Files
- Sender:
  - local_keylog.txt – Plaintext keylogs
  - local_encrypted_keylog.txt – Encrypted keylogs

- Receiver:
  - received_decrypted_keylog.txt – Decrypted output
  - received_encrypted_keylog.txt – Raw encrypted logs

--

## ⚠️ Legal & Ethical Notice
This project is intended solely for educational and authorized penetration testing in controlled environments. Unauthorized use of keyloggers may be illegal and unethical.

Always obtain explicit written permission before deploying in any environment that you do not own or control.

--

## 📜 License
This project is open-source under the MIT License[License].
