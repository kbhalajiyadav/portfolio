#!/usr/bin/env python3
"""Notify IndexNow-compatible search engines after a successful deployment."""
from __future__ import annotations

import json
import sys
import urllib.request

HOST = "bhalaji.com"
KEY = "8fb5b8e8103c4be597843ff2e7860f4a"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
URLS = [
    f"https://{HOST}/",
    f"https://{HOST}/research/",
    f"https://{HOST}/publication/adhesives-wearable/",
    f"https://{HOST}/publication/electrospun-fiber-mats/",
    f"https://{HOST}/publication/masters-thesis/",
    f"https://{HOST}/project/peel-trace-evaluation/",
    f"https://{HOST}/llms.txt",
    f"https://{HOST}/llms-full.txt",
]

payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": URLS,
}).encode("utf-8")
request = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=payload,
    headers={"Content-Type": "application/json; charset=utf-8"},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=20) as response:
        print(f"IndexNow response: {response.status}")
except Exception as exc:
    print(f"IndexNow notification failed: {exc}", file=sys.stderr)
    raise SystemExit(1)
