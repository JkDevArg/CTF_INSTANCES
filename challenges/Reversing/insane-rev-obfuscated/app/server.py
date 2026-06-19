from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>ObfCorp — Python Layers</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0a0a0a;
      color: #00ff41;
      font-family: 'Courier New', Courier, monospace;
      padding: 40px 20px;
    }
    .container { max-width: 720px; margin: 0 auto; }
    h1 { color: #00ff41; font-size: 1.6rem; margin-bottom: 6px; letter-spacing: 1px; }
    .tag {
      display: inline-block;
      background: #1a0033;
      color: #cc00ff;
      font-size: 0.7rem;
      padding: 2px 10px;
      border-radius: 2px;
      margin-bottom: 24px;
      text-transform: uppercase;
      border: 1px solid #cc00ff;
    }
    .story {
      background: #0d0d0d;
      border-left: 3px solid #cc00ff;
      padding: 16px 20px;
      margin-bottom: 24px;
      line-height: 1.9;
      color: #aa00dd;
      font-style: italic;
    }
    .desc { color: #00aa22; line-height: 1.8; margin-bottom: 28px; }
    .desc code {
      color: #cc00ff;
      background: #0d001a;
      padding: 1px 5px;
      border-radius: 2px;
    }
    .layers {
      background: #0d0d0d;
      border: 1px solid #1a0033;
      border-radius: 4px;
      padding: 14px 20px;
      margin-bottom: 24px;
      font-size: 0.82rem;
      color: #660099;
      line-height: 2;
    }
    .layers span { color: #cc00ff; }
    .download-btn {
      display: inline-block;
      background: #1a0033;
      color: #cc00ff;
      text-decoration: none;
      padding: 12px 28px;
      border-radius: 4px;
      font-size: 1rem;
      border: 1px solid #cc00ff;
      transition: background 0.15s;
    }
    .download-btn:hover { background: #2a0055; }
    .info {
      background: #0d0d0d;
      border: 1px solid #1a0033;
      border-radius: 4px;
      padding: 16px 20px;
      margin-top: 28px;
      font-size: 0.85rem;
      color: #660099;
    }
    .info h3 { color: #cc00ff; font-size: 0.9rem; margin-bottom: 8px; }
    .prompt { color: #330066; margin-top: 24px; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&gt; ObfCorp &mdash; Python Layers</h1>
    <span class="tag">insane &bull; reversing &bull; obfuscation</span>
    <div class="story">
      <p>ObfCorp prot&eacute;ge su checker con capas.</p>
      <p>Cada capa oculta la siguiente. La l&oacute;gica final es simple.</p>
      <p>El camino para llegar a ella, no tanto.</p>
    </div>
    <p class="desc">
      Un script Python verifica tu input &mdash; pero el c&oacute;digo fuente ha sido procesado.<br>
      Tres capas de <code>base64</code> &rarr; <code>zlib</code> &rarr; <code>marshal</code> &rarr; <code>exec</code> anidado.<br><br>
      Desenvuelve cada capa, analiza el bytecode, y llega al n&uacute;cleo.
    </p>
    <div class="layers">
      <span>Capa 0</span> &rarr; base64 + zlib + marshal + exec<br>
      <span>Capa 1</span> &rarr; base64 + zlib + marshal + exec<br>
      <span>Capa 2</span> &rarr; base64 + zlib + marshal + exec<br>
      <span>Capa 3</span> &rarr; <em style="color:#440066">??? la logica real</em>
    </div>
    <a href="/download/checker.py" class="download-btn">&#11015; Descargar checker.py</a>
    <div class="info">
      <h3>// Pista</h3>
      <p>Lo que <code>exec()</code> puede ejecutar, el ojo humano tambi&eacute;n puede leer &mdash;
      con paciencia.<br>
      El m&oacute;dulo <code>dis</code> de Python es tu linterna en la oscuridad.</p>
    </div>
    <p class="prompt">$ _</p>
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
    app.run(host='0.0.0.0', port=80, debug=False)
