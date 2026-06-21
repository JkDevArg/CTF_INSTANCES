import os, json
from flask import Flask, send_from_directory, render_template_string, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

app = Flask(__name__)

# Load key generated at startup
with open('/tmp/oracle_key.bin', 'rb') as f:
    KEY = f.read()

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>CipherCorp — Padding Oracle</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}.hint{color:#009920;font-style:italic}pre{background:#001100;padding:12px;font-size:.85rem;overflow-x:auto}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}</style></head><body>
<h1>CipherCorp &mdash; AES-CBC Decryption Service</h1>
<div class="box"><p>El servicio acepta ciphertext AES-CBC y responde si el padding es v&aacute;lido o no.<br>Un mensaje fue interceptado. Descifr&aacute;lo usando el or&aacute;culo.</p></div>
<div class="box"><h2>Descargas</h2><ul style="padding-left:20px"><li><a href="/download/intercepted.json">intercepted.json &mdash; ciphertext interceptado + info del or&aacute;culo</a></li></ul></div>
<div class="box"><h2>Or&aacute;culo</h2>
<pre>POST /oracle
Content-Type: application/json
{"iv": "&lt;hex&gt;", "ciphertext": "&lt;hex&gt;"}

Respuesta:
{"valid": true}   &larr; padding correcto
{"valid": false}  &larr; padding inv&aacute;lido (o error)</pre></div>
<div class="box"><p class="hint">El error de padding habla m&aacute;s que cualquier mensaje cifrado.</p></div>
</body></html>"""

@app.route('/')
def index(): return render_template_string(PAGE)

@app.route('/download/<path:f>')
def download(f): return send_from_directory('/app/dist', f, as_attachment=True)

@app.route('/oracle', methods=['POST'])
def oracle():
    try:
        data       = request.get_json(force=True)
        iv         = bytes.fromhex(data['iv'])
        ciphertext = bytes.fromhex(data['ciphertext'])
        cipher     = AES.new(KEY, AES.MODE_CBC, iv)
        plaintext  = cipher.decrypt(ciphertext)
        unpad(plaintext, 16)        # raises ValueError on bad padding
        return jsonify({'valid': True})
    except Exception:
        return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
