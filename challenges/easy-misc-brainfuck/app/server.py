import os
from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>BrainMatic — Ejecutor de Codigo</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 40px; }
    h1 { color: #00ff41; border-bottom: 1px solid #00ff41; padding-bottom: 12px; margin-bottom: 24px; }
    h2 { color: #00ff41; margin-bottom: 12px; }
    .box { border: 1px solid #003300; background: #050505; padding: 20px; margin-bottom: 20px; }
    a { color: #00ff41; }
    a:hover { color: #00cc33; }
    .hint { color: #009920; font-style: italic; }
    ul { padding-left: 20px; }
    li { margin: 8px 0; }
    code { background: #111; padding: 2px 6px; border: 1px solid #003300; }
  </style>
</head>
<body>
  <h1>&#x25a0; BrainMatic &mdash; Ejecutor de Codigo</h1>
  <div class="box">
    <p>Se encontro un programa escrito en un lenguaje muy peculiar.<br>
    Ejecútalo para ver qué contiene.<br>
    Se incluye el intérprete; solo necesitas Python 3.</p>
  </div>
  <div class="box">
    <h2>Descargas</h2>
    <ul>
      <li><a href="/download/program.bf">program.bf</a> &mdash; El programa misterioso</li>
      <li><a href="/download/bf.py">bf.py</a> &mdash; Intérprete Python incluido</li>
    </ul>
  </div>
  <div class="box">
    <p>Instrucciones de uso:</p>
    <p style="margin-top:12px"><code>python3 bf.py program.bf</code></p>
  </div>
  <div class="box">
    <p class="hint">Las células de memoria guardan secretos. El que sepa ejecutar el código, los descubrirá.</p>
  </div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download/<path:f>')
def download(f):
    return send_from_directory('/app/dist', f, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
