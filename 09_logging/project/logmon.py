#!/usr/bin/env python3
"""Log monitoring daemon — watches a log file for patterns, sends alerts, rotates."""

import argparse
import logging
import logging.handlers
import os
import re
import sys
import time
from typing import Optional


class PatternAlertFilter(logging.Filter):
    """Custom filter that checks for alert patterns in log records."""

    def __init__(self, patterns: list[str], name: str = ""):
        super().__init__(name)
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        for pat in self.patterns:
            if pat.search(msg):
                return True
        return False


class AlertHandler(logging.Handler):
    """Handler that simulates sending alerts (print to stderr by default)."""

    def __init__(self, alert_file: Optional[str] = None):
        super().__init__()
        self.setLevel(logging.WARNING)
        self.alert_file = alert_file

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        alert_line = f"[ALERT] {msg}\n"
        if self.alert_file:
            with open(self.alert_file, "a") as fh:
                fh.write(alert_line)
        else:
            sys.stderr.write(alert_line)
            sys.stderr.flush()


def setup_logger(
    log_file: str,
    patterns: list[str],
    alert_file: Optional[str] = None,
    rotate_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    logger = logging.getLogger("logmon")
    logger.setLevel(logging.DEBUG)

    # Rotating file handler for the monitor's own log
    fh = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=rotate_bytes, backupCount=backup_count
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(ch)

    # Alert handler with pattern filter
    alert = AlertHandler(alert_file)
    alert.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    if patterns:
        alert.addFilter(PatternAlertFilter(patterns))
    logger.addHandler(alert)

    return logger


def watch_file(
    path: str,
    logger: logging.Logger,
    poll_interval: float = 1.0,
    follow: bool = True,
) -> int:
    """Watch a log file for new lines and log them through the monitor."""
    if not os.path.exists(path):
        logger.error("Log file not found: %s", path)
        return 1

    logger.info("Watching: %s", path)

    try:
        with open(path, "r") as fh:
            # Seek to end unless we want existing content
            if follow:
                fh.seek(0, os.SEEK_END)

            while True:
                line = fh.readline()
                if line:
                    line = line.rstrip("\n")
                    logger.info(line)
                else:
                    time.sleep(poll_interval)
    except KeyboardInterrupt:
        logger.info("Shutting down monitor.")
    except Exception as exc:
        logger.error("Error watching file: %s", exc)
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Log monitoring daemon — watches a log file for patterns and sends alerts.",
    )
    parser.add_argument("logfile", help="Log file to monitor")
    parser.add_argument(
        "--monitor-log",
        default="logmon.log",
        help="File for the monitor's own log (default: logmon.log)",
    )
    parser.add_argument(
        "--pattern",
        action="append",
        default=[],
        metavar="REGEX",
        help="Alert on lines matching REGEX (can repeat)",
    )
    parser.add_argument(
        "--alert-file",
        default=None,
        help="Write alerts to this file instead of stderr",
    )
    parser.add_argument(
        "--rotate-bytes",
        type=int,
        default=10 * 1024 * 1024,
        help="Max bytes before rotating monitor log (default: 10 MB)",
    )
    parser.add_argument(
        "--backup-count",
        type=int,
        default=5,
        help="Number of rotated monitor log backups (default: 5)",
    )
    parser.add_argument(
        "--poll",
        type=float,
        default=1.0,
        help="Poll interval in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--no-follow",
        action="store_true",
        help="Do not seek to end; process existing content",
    )

    args = parser.parse_args()

    logger = setup_logger(
        log_file=args.monitor_log,
        patterns=args.pattern,
        alert_file=args.alert_file,
        rotate_bytes=args.rotate_bytes,
        backup_count=args.backup_count,
    )

    return watch_file(
        path=args.logfile,
        logger=logger,
        poll_interval=args.poll,
        follow=not args.no_follow,
    )


if __name__ == "__main__":
    sys.exit(main())
