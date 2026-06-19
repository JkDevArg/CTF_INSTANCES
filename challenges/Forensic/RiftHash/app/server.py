from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>RiftHash &mdash; Crackme</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 700px; margin: 0 auto; }
    h1 { color: #3fb950; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #1a4d2e; color: #3fb950; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; border: 1px solid #3fb950; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .btn-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 28px; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-size: 0.95rem; }
    .download-btn:hover { background: #2ea043; }
    .download-btn.secondary { background: #21262d; border: 1px solid #30363d; }
    .download-btn.secondary:hover { background: #30363d; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 4px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#128274; RiftHash &mdash; Crackme</h1>
    <span class="tag">medium &bull; forensic</span>
    <p class="desc">
      Un sistema de autenticaci&oacute;n personalizado usa un algoritmo propietario.<br>
      Interceptaste el hash de la contrase&ntilde;a. El algoritmo tambi&eacute;n est&aacute; disponible.<br>
      La contrase&ntilde;a que produce el hash <strong style="color:#c9d1d9">es la flag</strong>.
    </p>
    <div class="btn-row">
      <a href="/download/hash" class="download-btn">&#11015; Descargar rifthash.hash</a>
      <a href="/download/algo" class="download-btn secondary">&#11015; Descargar rifthash.py</a>
    </div>
    <div class="info">
      <h3>Hint</h3>
      <ul style="padding-left:18px; line-height:2;">
        <li>65536 iteraciones ralentizan el ataque de fuerza bruta. Pero el espacio de b&uacute;squeda puede ser peque&ntilde;o.</li>
      </ul>
    </div>
  </div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download/hash')
def download_hash():
    return send_file('/app/dist/rifthash.hash', as_attachment=True, download_name='rifthash.hash')


@app.route('/download/algo')
def download_algo():
    return send_file('/app/dist/rifthash.py', as_attachment=True, download_name='rifthash.py')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
