# System Programming — Process management, OS signals, encryption, system monitoring

## Quick Start
```bash
# Battery status monitor + desktop notification
python 13_battery.py

# Internet connectivity check (dual method: urllib + socket)
python 13_check_internet.py

# Fetch remote SSL/TLS certificates via OpenSSL
python 13_remote_cert.py google.com:443

# Find running processes by name
python 13_processes.py                       # edit process_name inside the file

# Stop a process by name (with optional delay in minutes)
python 13_stop_process.py --name firefox --delay 5

# Signal handling: SIGINT (Ctrl+C) and SIGTSTP (Ctrl+Z)
python python_signals/signal_example.py

# Signal class wrapper + alarm signal + valid signal listing
python python_signals/signal_class.py
python python_signals/alarm_signal.py
python python_signals/valid_signals.py

# Symmetric encryption with Fernet (cryptography library)
python encriptacion/fernet_cipher.py

# MD5 checksum utilities + Atbash cipher
python encriptacion/md5_checksum.py
python encriptacion/atbash-cipher.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `13_battery.py` | System sensors via `psutil`, desktop notifications | `psutil.sensors_battery()`, `notifypy.Notify().send()` |
| `13_check_internet.py` | Network connectivity detection | `urllib.request.urlopen('http://google.com')`, `socket.gethostbyname()` |
| `13_remote_cert.py` | Shell out to OpenSSL for cert fetching | `subprocess.Popen("openssl s_client …")`, regex extraction of PEM cert |
| `13_processes.py` | Process discovery via pgrep + /proc filesystem | `subprocess.check_output(["pgrep", "-f", name])`, `os.system("ps u -p PID")` |
| `13_stop_process.py` | Process lifecycle management with Click CLI | Click app with `--name`/`--delay` options, `psutil.Process(pid).terminate()` |
| `python_signals/signal_example.py` | Registering handlers for SIGINT/SIGTSTP | `signal.signal(signal.SIGINT, handler)`, handler receives `(signum, frame)` |
| `python_signals/signal_class.py` | OOP wrapper for signal handling | Class-based signal handler registration |
| `python_signals/alarm_signal.py` | `signal.SIGALRM` for timeout patterns | `signal.alarm(seconds)`, alarm signal callback |
| `python_signals/valid_signals.py` | Enumerating available signals | Listing all valid signal names on the current platform |
| `encriptacion/fernet_cipher.py` | Symmetric encryption with Fernet | `Fernet.generate_key()`, `.encrypt(msg.encode())`, `.decrypt(data)`, key file management |
| `encriptacion/werkzeug_example.py` | Hashing with Werkzeug | `werkzeug.security.generate_password_hash/check_password_hash` |
| `encriptacion/md5_checksum.py` | File integrity via MD5 checksums | `hashlib.md5()`, compare checksums for file validation |

> **Files:** 16 files across `python_signals/`, `encriptacion/`, and top-level concept directory.

## Common Patterns
```python
# Process management with psutil
import psutil
for proc in psutil.process_iter(["pid", "name"]):
    if "firefox" in proc.info["name"]:
        psutil.Process(proc.info["pid"]).terminate()

# Signal handling
import signal
def handler(signum, frame):
    print(f"Received signal {signum}")
    exit(0)
signal.signal(signal.SIGINT, handler)     # Ctrl+C
signal.signal(signal.SIGTSTP, handler)    # Ctrl+Z

# Fernet symmetric encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"secret message")
decrypted = cipher.decrypt(encrypted).decode()

# Battery monitor
battery = psutil.sensors_battery()
if battery.power_plugged:
    print(f"Charging: {battery.percent:.1f}%")
```

## Now Build Your Own
**Challenge:** Write a `sys_monitor.py` daemon that checks battery level every 30 seconds. If battery drops below 20% and is NOT plugged in, send a desktop notification and log a warning to a file. If battery drops below 5%, send a critical notification and save a timestamped alert. Use `signal.SIGTERM` to gracefully shut down.
