from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>RSACorp — Wiener's Attack</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}a:hover{color:#fff}.hint{color:#009920;font-style:italic}pre{background:#001100;padding:12px;font-size:.85rem}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}</style></head><body>
<h1>RSACorp &mdash; Decryption Service</h1>
<div class="box"><p>Un mensaje fue cifrado con RSA. La clave p&uacute;blica est&aacute; disponible.<br>
El administrador insisti&oacute; en usar un exponente privado peque&ntilde;o para &quot;mejorar el rendimiento&quot;.</p></div>
<div class="box"><h2>Descargas</h2><ul style="padding-left:20px">
<li><a href="/download/wiener.txt">wiener.txt &mdash; n, e y ciphertext RSA</a></li>
</ul></div>
<div class="box"><h2>Pista criptogr&aacute;fica</h2>
<pre>Teorema de Wiener (1990):
Si d &lt; n^0.25 / 3, entonces d puede recuperarse
mediante la expansion en fracciones continuas de e/n.

Las fracciones continuas convierten un numero racional
en una secuencia de convergentes k/d que aproximan e/n.
Uno de esos convergentes revela d exactamente.</pre></div>
<div class="box"><p class="hint">La eficiencia es el enemigo de la seguridad cuando se aplica al exponente equivocado.</p></div>
</body></html>"""


@app.route('/')
def index(): return render_template_string(PAGE)


@app.route('/download/<path:f>')
def download(f): return send_from_directory('/app/dist', f, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
