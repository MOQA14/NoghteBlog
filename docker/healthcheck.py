#!/usr/bin/env python
"""
بررسی سلامت کانتینر وب.

در docker-compose.yaml به‌صورت «python /app/docker/healthcheck.py» صدا زده می‌شود.

چرا به این سادگی نیست که یک درخواست ساده بزنیم:
  • تنظیمات پروداکشن SECURE_SSL_REDIRECT دارد، پس درخواست http پاسخ ۳۰۱ می‌گیرد.
    هدر X-Forwarded-Proto: https همان کاری را می‌کند که traefik می‌کند.
  • ALLOWED_HOSTS شامل 127.0.0.1 نیست، پس بدون هدر Host پاسخ ۴۰۰ می‌گیریم.
    اولین دامنه‌ی ALLOWED_HOSTS به‌عنوان Host فرستاده می‌شود.

خروجی ۰ یعنی سالم، هر چیز دیگری یعنی ناسالم.
"""

import os
import sys
import urllib.error
import urllib.request

PORT = os.environ.get("HEALTHCHECK_PORT", "8000")
TIMEOUT = float(os.environ.get("HEALTHCHECK_TIMEOUT", "5"))


def first_allowed_host():
    hosts = os.environ.get("ALLOWED_HOSTS", "")
    for host in hosts.split(","):
        host = host.strip()
        if host and host != "*":
            return host
    return "localhost"


def main():
    request = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/",
        headers={"Host": first_allowed_host(), "X-Forwarded-Proto": "https"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            if response.status == 200:
                return 0
            print(f"unhealthy: status {response.status}", file=sys.stderr)
    except urllib.error.HTTPError as exc:
        print(f"unhealthy: status {exc.code}", file=sys.stderr)
    except Exception as exc:
        print(f"unhealthy: {exc}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
