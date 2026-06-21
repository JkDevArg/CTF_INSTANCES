from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>AntiDbg Corp — Anti-Debug Crackme</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0a0a0a;
      color: #00ff41;
      font-family: 'Courier New', Courier, monospace;
      padding: 40px 20px;
    }
    .container { max-width: 720px; margin: 0 auto; }
    h1 { color: #ff4400; font-size: 1.6rem; margin-bottom: 6px; letter-spacing: 1px; }
    .tag {
      display: inline-block;
      background: #1a0000;
      color: #ff4400;
      font-size: 0.7rem;
      padding: 2px 10px;
      border-radius: 2px;
      margin-bottom: 24px;
      text-transform: uppercase;
      border: 1px solid #ff4400;
    }
    .story {
      background: #0d0d0d;
      border-left: 3px solid #ff4400;
      padding: 16px 20px;
      margin-bottom: 24px;
      line-height: 1.9;
      color: #cc3300;
      font-style: italic;
    }
    .desc { color: #00aa22; line-height: 1.8; margin-bottom: 28px; }
    .desc code {
      color: #ff4400;
      background: #1a0000;
      padding: 1px 5px;
      border-radius: 2px;
    }
    .protections {
      background: #0d0d0d;
      border: 1px solid #1a0000;
      border-radius: 4px;
      padding: 14px 20px;
      margin-bottom: 24px;
      font-size: 0.82rem;
      color: #660000;
      line-height: 2;
    }
    .protections .prot { color: #ff4400; }
    .download-btn {
      display: inline-block;
      background: #1a0000;
      color: #ff4400;
      text-decoration: none;
      padding: 12px 28px;
      border-radius: 4px;
      font-size: 1rem;
      border: 1px solid #ff4400;
      transition: background 0.15s;
    }
    .download-btn:hover { background: #330000; }
    .info {
      background: #0d0d0d;
      border: 1px solid #1a0000;
      border-radius: 4px;
      padding: 16px 20px;
      margin-top: 28px;
      font-size: 0.85rem;
      color: #550000;
    }
    .info h3 { color: #ff4400; font-size: 0.9rem; margin-bottom: 8px; }
    .prompt { color: #330000; margin-top: 24px; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&gt; AntiDbg Corp v2 &mdash; Access Control</h1>
    <span class="tag">insane &bull; reversing &bull; anti-debug</span>
    <div class="story">
      <p>AntiDbg Corp prot&eacute;ge su binario con defensas activas.</p>
      <p>El debugger es el enemigo. El tiempo, un testigo.</p>
      <p>La clave existe &mdash; pero el binario sabe si lo est&aacute;s mirando.</p>
    </div>
    <p class="desc">
      Un crackme con protecciones anti-debugging.<br>
      Si detecta un debugger o una ejecuci&oacute;n lenta, termina antes de llegar a la verificaci&oacute;n.<br><br>
      La flag est&aacute; codificada con <code>XOR 0x1F</code> en el segmento de datos.<br>
      Parchea, bypasea, o analiza est&aacute;ticamente.
    </p>
    <div class="protections">
      <span class="prot">[CHECK 1]</span> ptrace self-check &mdash; detecta si un debugger est&aacute; adjunto<br>
      <span class="prot">[CHECK 2]</span> timing check &mdash; detecta ejecuci&oacute;n paso a paso<br>
      <span class="prot">[PAYLOAD]</span> encoded_flag[] XOR 0x1F &mdash; en .data del binario
    </div>
    <a href="/download/antidbg" class="download-btn">&#11015; Descargar antidbg (ELF x86-64)</a>
    <div class="info">
      <h3>// Pista</h3>
      <p>No todo lo que el binario esconde requiere ejecutarlo.<br>
      Lo que est&aacute; en <code>.data</code> puede leerse sin correr nada &mdash;
      si sabes d&oacute;nde mirar.</p>
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
