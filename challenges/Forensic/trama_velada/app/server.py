from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Trama Velada</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 680px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #1f6feb; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .btn-group { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 0; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#128268; Trama Velada</h1>
    <span class="tag">hard &bull; forensic</span>
    <p class="desc">
      El tráfico fue capturado. El cifrado oculta su contenido. Pero las claves fueron recuperadas.
      Ahora depende de ti reconstruir lo que viajó por el cable.
    </p>
    <div class="btn-group">
      <a href="/download/pcap" class="download-btn">&#11015; Download traffic.pcap</a>
      <a href="/download/keylog" class="download-btn">&#11015; Download keylog.txt</a>
    </div>
    <div class="info">
      <h3>Hint</h3>
      <p>Wireshark sabe cómo usar claves de sesión TLS. Busca lo que viajó en los flujos HTTP.</p>
    </div>
  </div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download/pcap')
def download_pcap():
    return send_file('/app/traffic.pcap', as_attachment=True, download_name='traffic.pcap')


@app.route('/download/keylog')
def download_keylog():
    return send_file('/app/keylog.txt', as_attachment=True, download_name='keylog.txt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
