# Networking — TCP/UDP sockets, email, web scraping, and HTTP clients

## Quick Start
```bash
# TCP sockets: basic server/client (run server first)
python Sockets/AT_server_v1.py                # terminal 1
python Sockets/AT_client_v1.py                # terminal 2

# Multi-client chat server with threading
python Sockets/BC_chat_server.py              # terminal 1
python Sockets/BC_chat_client.py              # terminal 2 (requires tkinter GUI)

# Socket server v2 (threaded, pickle serialization)
python Sockets/server-v2.py

# Send email via SMTP_SSL
python 12_send_email.py                       # requires .env with smtp config

# Parse mailer-daemon bounce messages
python 12_mailerdaemon.py

# Scrape Hacker News + email digest
python 12_news_parser.py

# BeautifulSoup HTML parsing deep-dive
python BeautifulSoup_examples/bs4_by_example.py
```

## Learning Path
| File | Concept | Key Pattern |
|------|---------|-------------|
| `Sockets/AT_server_v1.py` | TCP socket server: bind → listen → accept → send/recv → close | `socket.socket()`, `.bind((host,port))`, `.listen(5)`, `.accept()` |
| `Sockets/AT_client_v1.py` | TCP socket client: connect → recv → subprocess → send response | `socket.connect((host,port))`, `subprocess.Popen` for remote execution |
| `Sockets/BC_chat_server.py` | Multi-client chat with threading, pickle serialization | Dedicated `accept_conn` + `process_conn` threads, `pickle.loads/dumps` |
| `Sockets/BC_chat_client.py` | Chat client with tkinter GUI | Socket in background thread, tkinter `Text`/`Entry` widgets for chat UI |
| `Sockets/server-v2.py` | Threaded TCP server with pickle messaging | `threading.Thread` per client, `pickle` for structured messages |
| `12_send_email.py` | SMTP over SSL with dataclass config | `smtplib.SMTP_SSL`, `ssl.create_default_context()`, `.login()/.sendmail()` |
| `12_mailerdaemon.py` | Regex-based mail bounce parser | `email.message_from_file`, multi-pattern regex extraction, error aggregation |
| `12_news_parser.py` | HTTP scraping + email delivery pipeline | `requests.get()`, `BeautifulSoup.find_all()`, `smtplib.SMTP` |
| `BeautifulSoup_examples/bs4_by_example.py` | Comprehensive BeautifulSoup navigation tutorial | `.find()/.find_all()`, `.contents/.children/.descendants`, `.parent/.parents`, siblings, regex filters |

> **Files:** 13 files across `Sockets/`, `BeautifulSoup_examples/`, and top-level concept directory.

## Common Patterns
```python
# TCP server boilerplate
import socket
sock = socket.socket()
sock.bind(("localhost", 9999))
sock.listen(5)
conn, addr = sock.accept()
data = conn.recv(1024)
conn.send(b"response")
conn.close()

# TCP client
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 9999))
sock.send(b"hello")
response = sock.recv(1024)

# Sending email with SMTP_SSL
import smtplib, ssl
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login("user@gmail.com", "app-password")
    server.sendmail(from_addr, to_addr, message)

# BeautifulSoup scraping
import requests
from bs4 import BeautifulSoup
soup = BeautifulSoup(requests.get(url).content, "html.parser")
for tag in soup.find_all("td", class_="title"):
    print(tag.text)
```

## Now Build Your Own
**Challenge:** Build a simple HTTP echo server using raw sockets. Accept connections on port 8888, read the HTTP request line, and respond with a valid HTTP 200 response containing a JSON body `{"method": "GET", "path": "/hello", "echo": "success"}`. Test with `curl http://localhost:8888/hello`. Handle multiple sequential requests on the same connection.
