import json
from flask import Flask, send_from_directory, render_template_string, request, jsonify

app = Flask(__name__)

with open('/tmp/rsa_lsb_key.json') as f:
    KEY = json.load(f)
N, D = KEY['n'], KEY['d']

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>LSB Oracle — RSACorp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}a:hover{color:#fff}.hint{color:#009920;font-style:italic}pre{background:#001100;padding:12px;font-size:.85rem;overflow-x:auto}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}</style></head><body>
<h1>RSACorp &mdash; LSB Decryption Oracle</h1>
<div class="box"><p>El servidor puede descifrar cualquier ciphertext RSA, pero solo revela si el resultado es par o impar.<br>Un mensaje fue cifrado. Rec&uacute;peralo con solo un bit por consulta.</p></div>
<div class="box"><h2>Descargas</h2><ul style="padding-left:20px">
<li><a href="/download/params.json">params.json &mdash; n, e y ciphertext original</a></li>
</ul></div>
<div class="box"><h2>Or&aacute;culo</h2>
<pre>POST /oracle
Content-Type: application/json
{"c": &lt;entero decimal&gt;}

Respuesta:
{"lsb": 0}   &larr; plaintext es par (bit menos significativo = 0)
{"lsb": 1}   &larr; plaintext es impar (bit menos significativo = 1)</pre></div>
<div class="box"><h2>Propiedad RSA relevante</h2>
<pre>Enc(2) * Enc(m) mod n = Enc(2m mod n)
Si 2m &lt; n  &rarr; LSB de 2m depende de m
Si 2m &ge; n &rarr; 2m - n cambia la paridad
Esta propiedad permite busqueda binaria.</pre></div>
<div class="box"><p class="hint">Con cada bit revelado, el universo de posibles mensajes se parte en dos.</p></div>
</body></html>"""


@app.route('/')
def index(): return render_template_string(PAGE)


@app.route('/download/<path:f>')
def download(f): return send_from_directory('/app/dist', f, as_attachment=True)


@app.route('/oracle', methods=['POST'])
def oracle():
    try:
        c = int(request.get_json(force=True)['c'])
        m = pow(c, D, N)
        return jsonify({'lsb': m & 1})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
