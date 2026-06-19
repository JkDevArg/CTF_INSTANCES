from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>StreamCorp — LFSR Cipher</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}a:hover{color:#fff}.hint{color:#009920;font-style:italic}pre{background:#001100;padding:12px;font-size:.85rem}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}</style></head><body>
<h1>StreamCorp &mdash; LFSR Stream Cipher</h1>
<div class="box"><p>Un cifrador de flujo basado en un LFSR de 16 bits fue usado para cifrar un mensaje confidencial.<br>El polinomio es conocido. El estado inicial, no. Pero el espacio de b&uacute;squeda es... manejable.</p></div>
<div class="box"><h2>Descargas</h2><ul style="padding-left:20px">
<li><a href="/download/stream.txt">stream.txt &mdash; polinomio, taps y ciphertext cifrado</a></li>
</ul></div>
<div class="box"><h2>Informaci&oacute;n del cifrador</h2>
<pre>Tipo:      LFSR Galois de 16 bits
Polinomio: x^16 + x^14 + x^13 + x^11 + 1
Taps:      0xB400
Espacio:   2^16 = 65 536 estados posibles
Prefijo:   HACKL4BS_CTF_ (texto plano conocido)</pre></div>
<div class="box"><p class="hint">Cuando conoces el principio del mensaje, el resto del keystream se revela.</p></div>
</body></html>"""


@app.route('/')
def index(): return render_template_string(PAGE)


@app.route('/download/<path:f>')
def download(f): return send_from_directory('/app/dist', f, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
