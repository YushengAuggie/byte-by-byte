#!/usr/bin/env python3
"""byte-by-byte: Send a message via Telegram with retry logic and exponential backoff.

Usage:
    python3 send-telegram.py <message>
    echo "message" | python3 send-telegram.py -

Exit codes:
    0 — message sent successfully
    1 — all retries exhausted (failure logged to logs/delivery.log)
"""

import sys
import os
import time
import subprocess
import json
import logging
from datetime import datetime, timezone

# ── Resolve paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR   = os.path.join(SCRIPT_DIR, '..')
LOGS_DIR   = os.path.join(REPO_DIR, 'logs')
LOG_FILE   = os.path.join(LOGS_DIR, 'delivery.log')

os.makedirs(LOGS_DIR, exist_ok=True)

# ── Logger: file + stderr ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)-8s  %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%SZ',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stderr),
    ],
)
log = logging.getLogger('send-telegram')

# ── Config ─────────────────────────────────────────────────────────────────────
def load_config():
    config = {}
    config_path = os.path.join(REPO_DIR, 'config.env')
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip().strip('"')
    return config

# ── Send via openclaw message tool ────────────────────────────────────────────
def send_message(message: str, target: str, openclaw_bin: str) -> bool:
    """Invoke openclaw to send a Telegram message. Returns True on success."""
    cmd = [
        openclaw_bin, 'message', 'send',
        '--channel', 'telegram',
        '--target', target,
        '--message', message,
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True
        log.warning('openclaw exited %d: %s', result.returncode, result.stderr.strip())
        return False
    except subprocess.TimeoutExpired:
        log.warning('openclaw timed out after 30s')
        return False
    except Exception as exc:
        log.warning('subprocess error: %s', exc)
        return False

# ── Retry loop ─────────────────────────────────────────────────────────────────
MAX_RETRIES   = 3
BACKOFF_SECS  = [2, 4, 8]   # exponential backoff delays

def send_with_retry(message: str, target: str, openclaw_bin: str) -> bool:
    for attempt in range(1, MAX_RETRIES + 1):
        log.info('Attempt %d/%d → target=%s', attempt, MAX_RETRIES, target)
        if send_message(message, target, openclaw_bin):
            log.info('✅ Delivered on attempt %d', attempt)
            return True
        if attempt < MAX_RETRIES:
            delay = BACKOFF_SECS[attempt - 1]
            log.warning('Attempt %d failed — retrying in %ds…', attempt, delay)
            time.sleep(delay)
        else:
            log.error('❌ All %d attempts failed', MAX_RETRIES)

    return False

# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == '-':
        message = sys.stdin.read().strip()
    else:
        message = ' '.join(sys.argv[1:])

    if not message:
        log.error('No message provided')
        sys.exit(1)

    config = load_config()
    target       = config.get('TELEGRAM_TARGET', '')
    openclaw_bin = config.get('OPENCLAW_BIN', 'openclaw')

    if not target:
        log.error('TELEGRAM_TARGET not set in config.env')
        sys.exit(1)

    log.info('Sending %d-char message to %s', len(message), target)
    success = send_with_retry(message, target, openclaw_bin)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
