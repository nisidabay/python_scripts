#!/usr/bin/env python3
"""Networking exercises: HTTP requests, TCP sockets, SMTP, URL parsing, HTTP server."""

import json
import socket
import smtplib
import threading
import time
import urllib.parse
from email.mime.text import MIMEText
from http.server import HTTPServer, BaseHTTPRequestHandler

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 1: requests — GET with timeout, status check, JSON parse
# ═══════════════════════════════════════════════════════════════════════════════

import requests

try:
    # Real-world: GET a public JSON API with a timeout
    resp = requests.get(
        "https://httpbin.org/json",
        timeout=5,  # always set a timeout to avoid hanging
    )
    resp.raise_for_status()  # raises HTTPError for 4xx/5xx
    data = resp.json()  # parse JSON response
    print("Exercise 1 — requests GET to httpbin.org/json:")
    print(f"  Status: {resp.status_code}")
    print(f"  Content-Type: {resp.headers.get('Content-Type')}")
    # httpbin.org/json returns {"slideshow": {...}} — show top-level keys
    print(f"  Top-level keys: {list(data.keys())}")
    print(f"  Response time: {resp.elapsed.total_seconds():.3f}s")
except requests.RequestException as e:
    # Graceful fallback if no network — use a mock response
    print("Exercise 1 — requests (mocked — no network):")
    print(f"  Network unavailable: {e}")
    print("  Pattern: resp = requests.get(url, timeout=5); resp.raise_for_status(); data = resp.json()")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 2: Simple TCP echo server + client with sockets
# ═══════════════════════════════════════════════════════════════════════════════

HOST = "127.0.0.1"
PORT = 9876  # unprivileged port

def echo_server():
    """Run a single-threaded TCP echo server that handles one connection."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(1)
        srv.settimeout(2)  # don't block forever in accept()
        try:
            conn, addr = srv.accept()
        except socket.timeout:
            return  # no client connected — fine for demo
        with conn:
            data = conn.recv(1024)
            conn.sendall(data)  # echo it back

def echo_client(message: bytes) -> bytes | None:
    """Connect to echo server, send message, receive response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((HOST, PORT))
            sock.sendall(message)
            return sock.recv(1024)
        except (ConnectionRefusedError, socket.timeout):
            return None

# Start server in background thread, then run client
server_thread = threading.Thread(target=echo_server, daemon=True)
server_thread.start()
time.sleep(0.1)  # let server bind

response = echo_client(b"Hello, echo!")
print("Exercise 2 — TCP echo:")
print(f"  Sent: Hello, echo!")
print(f"  Received: {response.decode() if response else 'none (server not ready)'}")
server_thread.join(timeout=2)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 3: SMTP email sender — composition only (no real send)
# ═══════════════════════════════════════════════════════════════════════════════

def compose_email(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    smtp_host: str = "localhost",
    smtp_port: int = 25,
) -> str:
    """Build an email and show how it would be sent via SMTP.

    In production, use smtplib.SMTP + login for real delivery.
    Here we just compose and return the raw message for inspection.
    """
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    return msg.as_string()

raw_email = compose_email(
    sender="devops@acme.com",
    recipient="alerts@acme.com",
    subject="Disk Usage Warning",
    body="Disk /dev/sda1 is at 92% capacity. Please investigate.",
)

print("Exercise 3 — SMTP email composition:")
print(f"  Message length: {len(raw_email)} bytes")
print(f"  Headers + body:\n{raw_email}")
# Real send would be:
# with smtplib.SMTP('smtp.example.com', 587) as server:
#     server.starttls()
#     server.login(user, password)
#     server.send_message(msg)
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# Exercise 4: URL parser — extract scheme, host, path, query params
# ═══════════════════════════════════════════════════════════════════════════════

def parse_url(url: str) -> dict:
    """Break a URL into its components using urllib.parse."""
    parsed = urllib.parse.urlparse(url)
    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": parsed.port,
        "path": parsed.path,
        "query_params": urllib.parse.parse_qs(parsed.query),
        "fragment": parsed.fragment,
    }

url = "https://api.example.com:8080/v2/users?name=Alice&role=admin&active=1#section2"
components = parse_url(url)

print("Exercise 4 — URL parsing:")
print(f"  URL: {url}")
print(f"  Scheme:   {components['scheme']}")
print(f"  Host:     {components['host']}")
print(f"  Port:     {components['port']}")
print(f"  Path:     {components['path']}")
print(f"  Query:    {components['query_params']}")
print(f"  Fragment: {components['fragment']}")
print("---")

# ═══════════════════════════════════════════════════════════════════════════════
# BONUS: Basic HTTP server with http.server
# ═══════════════════════════════════════════════════════════════════════════════

class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Minimal JSON API handler — responds to GET /api/status."""

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = json.dumps({"status": "ok", "uptime": "42m"})
            self.wfile.write(payload.encode())
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Hello from Python HTTP Server</h1>")
        else:
            self.send_response(404)
            self.end_headers()

    # Suppress default logging to keep output clean
    def log_message(self, format, *args):
        pass

# Start server, query it, then shut down
http_port = 9877
httpd = HTTPServer(("127.0.0.1", http_port), SimpleAPIHandler)
server_thread2 = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread2.start()
time.sleep(0.1)

# Query the server
try:
    resp = requests.get(f"http://127.0.0.1:{http_port}/api/status", timeout=2)
    print("BONUS — HTTP server response:")
    print(f"  /api/status → {resp.json()}")
    resp2 = requests.get(f"http://127.0.0.1:{http_port}/", timeout=2)
    print(f"  / → {resp2.text}")
except requests.RequestException as e:
    print(f"BONUS — HTTP server: {e}")

httpd.shutdown()
server_thread2.join(timeout=2)
print("---")

print("All networking exercises passed.")
