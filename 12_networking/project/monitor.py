#!/usr/bin/env python3
"""Simple HTTP health checker — reads URLs from file, checks status, sends email alert on failure."""

import argparse
import json
import smtplib
import socket
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional


@dataclass
class CheckResult:
    url: str
    status: Optional[int] = None
    elapsed: float = 0.0
    error: Optional[str] = None


def check_url(url: str, timeout: float = 10.0) -> CheckResult:
    """Perform a single HTTP health check."""
    start = time.monotonic()
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "health-checker/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.monotonic() - start
            return CheckResult(url=url, status=resp.status, elapsed=elapsed)
    except urllib.error.HTTPError as exc:
        elapsed = time.monotonic() - start
        return CheckResult(url=url, status=exc.code, elapsed=elapsed)
    except Exception as exc:
        elapsed = time.monotonic() - start
        return CheckResult(url=url, elapsed=elapsed, error=str(exc))


def load_urls(source: str) -> list[str]:
    """Load URLs from a file (one per line) or a JSON list."""
    path = Path(source)
    if not path.exists():
        print(f"Error: file not found: {source}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text().strip()

    # Try JSON
    if content.startswith("["):
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

    # Plain text, one URL per line
    return [line.strip() for line in content.splitlines() if line.strip()]


def send_email_alert(
    smtp_host: str,
    smtp_port: int,
    sender: str,
    recipients: list[str],
    subject: str,
    body: str,
    use_tls: bool = True,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> bool:
    """Send an email alert via SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)

    try:
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)

        if username and password:
            server.login(username, password)

        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        return True
    except Exception as exc:
        print(f"Email send failed: {exc}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HTTP health checker — check URL status and send alerts on failure.",
    )
    parser.add_argument(
        "source",
        help="File containing URLs (one per line or JSON array)",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0,
        help="Request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--retries", type=int, default=1,
        help="Retries per URL on failure (default: 1)",
    )
    parser.add_argument(
        "--interval", type=float, default=0.5,
        help="Delay between checks in seconds (default: 0.5)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results as JSON",
    )

    # Email alert options
    email = parser.add_argument_group("email alerts")
    email.add_argument("--smtp-host", help="SMTP server host")
    email.add_argument("--smtp-port", type=int, default=587, help="SMTP port (default: 587)")
    email.add_argument("--sender", help="Sender email address")
    email.add_argument("--recipients", nargs="+", help="Recipient email addresses")
    email.add_argument("--smtp-user", help="SMTP username")
    email.add_argument("--smtp-pass", help="SMTP password")
    email.add_argument("--no-tls", action="store_true", help="Disable STARTTLS")

    args = parser.parse_args()

    urls = load_urls(args.source)
    if not urls:
        print("Error: no URLs found in source file", file=sys.stderr)
        return 1

    print(f"Checking {len(urls)} URL(s)...")
    results: list[CheckResult] = []

    for url in urls:
        result = None
        for attempt in range(args.retries + 1):
            result = check_url(url, args.timeout)
            if result.error is None:
                break
            if attempt < args.retries:
                time.sleep(1)

        results.append(result)  # type: ignore[arg-type]
        if args.interval:
            time.sleep(args.interval)

    # Report
    ok = [r for r in results if r.error is None and r.status is not None and 200 <= r.status < 400]
    warn = [r for r in results if r.error is None and r.status is not None and (r.status < 200 or r.status >= 400)]
    fail = [r for r in results if r.error is not None]

    if args.json_output:
        output = []
        for r in results:
            output.append({
                "url": r.url,
                "status": r.status,
                "elapsed": round(r.elapsed, 3),
                "error": r.error,
            })
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Health Check Results: {len(ok)} OK, {len(warn)} warning, {len(fail)} failed")
        print(f"{'='*60}")
        for r in sorted(results, key=lambda x: (0 if x.error is None else 1, x.status or 0)):
            if r.error:
                print(f"  ✗ FAIL  {r.elapsed:.2f}s  {r.url}")
                print(f"          {r.error}")
            elif r.status and (r.status < 200 or r.status >= 400):
                print(f"  ⚠ WARN  {r.status}  {r.elapsed:.2f}s  {r.url}")
            else:
                print(f"  ✓ OK    {r.status}  {r.elapsed:.2f}s  {r.url}")

    # Send email alert on failure
    if (warn or fail) and args.smtp_host and args.sender and args.recipients:
        body_lines = ["Health check failures detected:\n"]
        for r in fail:
            body_lines.append(f"  FAIL: {r.url} — {r.error}")
        for r in warn:
            body_lines.append(f"  WARN: {r.url} — HTTP {r.status}")
        body = "\n".join(body_lines)

        hostname = socket.gethostname()
        subject = f"[Health Check] {len(fail)} failures, {len(warn)} warnings on {hostname}"

        print(f"\nSending alert email to {', '.join(args.recipients)}...")
        success = send_email_alert(
            smtp_host=args.smtp_host,
            smtp_port=args.smtp_port,
            sender=args.sender,
            recipients=args.recipients,
            subject=subject,
            body=body,
            use_tls=not args.no_tls,
            username=args.smtp_user,
            password=args.smtp_pass,
        )
        if success:
            print("Alert sent.")
        else:
            print("Alert failed to send.", file=sys.stderr)
            return 2

    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
