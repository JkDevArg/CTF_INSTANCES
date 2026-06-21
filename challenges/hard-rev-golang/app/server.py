from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>GoCorp — GoCrackMe v1.0</title>
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
      background: #003300;
      color: #00ff41;
      font-size: 0.7rem;
      padding: 2px 10px;
      border-radius: 2px;
      margin-bottom: 24px;
      text-transform: uppercase;
      border: 1px solid #00ff41;
    }
    .story {
      background: #0d0d0d;
      border-left: 3px solid #00ff41;
      padding: 16px 20px;
      margin-bottom: 24px;
      line-height: 1.9;
      color: #00cc33;
      font-style: italic;
    }
    .desc { color: #00aa22; line-height: 1.8; margin-bottom: 28px; }
    .desc code {
      color: #00ff41;
      background: #0d1a0d;
      padding: 1px 5px;
      border-radius: 2px;
    }
    .download-btn {
      display: inline-block;
      background: #003300;
      color: #00ff41;
      text-decoration: none;
      padding: 12px 28px;
      border-radius: 4px;
      font-size: 1rem;
      border: 1px solid #00ff41;
      transition: background 0.15s;
    }
    .download-btn:hover { background: #005500; }
    .info {
      background: #0d0d0d;
      border: 1px solid #003300;
      border-radius: 4px;
      padding: 16px 20px;
      margin-top: 28px;
      font-size: 0.85rem;
      color: #007700;
    }
    .info h3 { color: #00ff41; font-size: 0.9rem; margin-bottom: 8px; }
    .prompt { color: #005500; margin-top: 24px; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&gt; GoCorp &mdash; GoCrackMe v1.0</h1>
    <span class="tag">hard &bull; reversing &bull; golang</span>
    <div class="story">
      <p>GoCorp desplegó su validador de acceso en Go.</p>
      <p>Sin source code. Sin debug symbols. Solo un binario estático.</p>
      <p>El compilador de Go es predecible &mdash; y la memoria no miente.</p>
    </div>
    <p class="desc">
      Un binario Go espera tu input y verifica si coincide con el secreto.<br>
      Go compila est&aacute;ticamente &mdash; el binario es grande, pero los secretos
      siempre dejan rastro en las secciones de datos.<br><br>
      Descarga el binario, an&aacute;lízalo con <code>strings</code>, <code>Ghidra</code>,
      o <code>GoReSym</code>, y encuentra la clave.
    </p>
    <a href="/download/gocrackme" class="download-btn">&#11015; Descargar gocrackme (ELF x86-64)</a>
    <div class="info">
      <h3>// Pista</h3>
      <p>El bytecode y las cadenas de Go no son tan silenciosas como parecen.<br>
      Donde hay una funci&oacute;n de decodificaci&oacute;n, hay algo que decodificar.</p>
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
