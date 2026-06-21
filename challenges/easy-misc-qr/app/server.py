import os
from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>QR Scanner — Lab 404</title>
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
  </style>
</head>
<body>
  <h1>&#x25a0; QR Scanner &mdash; Lab 404</h1>
  <div class="box">
    <p>Se encontro un codigo QR en los archivos incautados.<br>
    Escanéalo o decodifícalo digitalmente para recuperar el mensaje.</p>
  </div>
  <div class="box">
    <h2>Descargas</h2>
    <ul>
      <li><a href="/download/codigo.png">codigo.png</a> &mdash; Imagen con el código QR</li>
    </ul>
  </div>
  <div class="box">
    <p class="hint">Lo que el ojo no puede leer en linea recta, la maquina lo interpreta en cuadrados.</p>
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
