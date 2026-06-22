from flask import Flask, send_file, render_template_string, request, jsonify
import os

app = Flask(__name__)
flag = "H4L{tls_gzip_xor_chain_2026}"

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
    .flag-section { margin-top: 32px; }
    .flag-section h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 12px; }
    .flag-input-wrap { display: flex; gap: 10px; flex-wrap: wrap; }
    .flag-input {
      flex: 1; min-width: 220px;
      background: #161b22; border: 1px solid #30363d;
      color: #c9d1d9; font-family: 'Courier New', monospace;
      font-size: 0.95rem; padding: 10px 14px; border-radius: 6px;
      outline: none; transition: border-color 0.2s;
    }
    .flag-input:focus { border-color: #58a6ff; }
    .flag-input.correct { border-color: #3fb950; }
    .flag-input.wrong   { border-color: #f85149; }
    .flag-btn {
      background: #1f6feb; color: white; border: none;
      padding: 10px 22px; border-radius: 6px; font-size: 0.95rem;
      font-family: 'Courier New', monospace; cursor: pointer; transition: background 0.2s;
    }
    .flag-btn:hover { background: #388bfd; }
    .flag-msg { margin-top: 10px; font-size: 0.85rem; min-height: 1.2em; }
    .flag-msg.err { color: #f85149; }
    .flag-result {
      display: none; margin-top: 16px;
      background: #0f2a1a; border: 1px solid #3fb950;
      border-radius: 6px; padding: 16px;
    }
    .flag-result p { color: #8b949e; font-size: 0.82rem; margin-bottom: 8px; }
    .flag-result code {
      display: block; color: #3fb950;
      font-size: 1.05rem; letter-spacing: 0.03em;
      word-break: break-all;
    }
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

    <div class="flag-section">
      <h3>&#127937; Enviar Flag</h3>
      <div class="flag-input-wrap">
        <input id="flagInput" class="flag-input" type="text"
               placeholder="H4L{...}" autocomplete="off" spellcheck="false" />
        <button class="flag-btn" onclick="checkFlag()">Verificar</button>
      </div>
      <p id="flagMsg" class="flag-msg"></p>
      <div id="flagResult" class="flag-result">
        <p>&#10003; &nbsp;¡Flag correcta! Esta es tu flag:</p>
        <code id="flagValue"></code>
      </div>
    </div>
  </div>

  <script>
    const input     = document.getElementById('flagInput');
    const msg       = document.getElementById('flagMsg');
    const resultBox = document.getElementById('flagResult');
    const flagValue = document.getElementById('flagValue');

    input.addEventListener('keydown', e => { if (e.key === 'Enter') checkFlag(); });

    async function checkFlag() {
      const value = input.value.trim();
      if (!value) return;

      try {
        const res  = await fetch('/check_flag', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ flag: value })
        });
        const data = await res.json();

        if (data.correct) {
          input.classList.remove('wrong');
          input.classList.add('correct');
          msg.className = 'flag-msg';
          msg.textContent = '';
          resultBox.style.display = 'block';
          flagValue.textContent = data.real_flag;
        } else {
          input.classList.remove('correct');
          input.classList.add('wrong');
          msg.className = 'flag-msg err';
          msg.textContent = '✘ Flag incorrecta. Sigue analizando el tráfico.';
          resultBox.style.display = 'none';
        }
      } catch {
        msg.className = 'flag-msg err';
        msg.textContent = 'Error de conexión al verificar.';
      }
    }
  </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/check_flag', methods=['POST'])
def check_flag():
    data = request.get_json(silent=True) or {}
    submitted = data.get('flag', '')
    if submitted == flag:
        return jsonify({'correct': True, 'real_flag': os.environ.get("FLAG")})
    return jsonify({'correct': False})

@app.route('/download/pcap')
def download_pcap():
    return send_file('/app/traffic.pcap', as_attachment=True, download_name='traffic.pcap')

@app.route('/download/keylog')
def download_keylog():
    return send_file('/app/keylog.txt', as_attachment=True, download_name='keylog.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)