import os
from flask import Flask, send_file, render_template_string, request, jsonify

app = Flask(__name__)

flag = "HL4{overpwnz_DS}"

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>OverDS</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 680px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #6e40c9; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .btn-group { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 0; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
    .flag-form { margin-top: 28px; }
    .flag-form input[type=text] {
      width: 100%; padding: 10px 14px; background: #161b22; border: 1px solid #30363d;
      border-radius: 6px; color: #c9d1d9; font-family: 'Courier New', monospace;
      font-size: 0.95rem; margin-bottom: 10px;
    }
    .flag-form button {
      background: #1f6feb; color: white; border: none; padding: 10px 24px;
      border-radius: 6px; font-size: 0.95rem; cursor: pointer;
    }
    .flag-form button:hover { background: #388bfd; }
    #flag-result { margin-top: 14px; padding: 12px 16px; border-radius: 6px; font-size: 0.9rem; display: none; }
    #flag-result.ok  { background: #0d2b1a; border: 1px solid #238636; color: #3fb950; }
    #flag-result.err { background: #2b0d0d; border: 1px solid #da3633; color: #f85149; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#127918; OverDS</h1>
    <span class="tag">easy &bull; forensic</span>
    <p class="desc">
      Una imagen descargada de una fuente sospechosa. No parece peligrosa.
      Pero lo que contiene adentro podría sorprenderte.
    </p>
    <div class="btn-group">
      <a href="/download/image" class="download-btn">&#11015; Download bajando_pepa.jpg</a>
    </div>
    <div class="flag-form">
      <h3>&#127937; Ingresa la flag</h3>
      <input type="text" id="flag-input" placeholder="HL4{...}" autocomplete="off" spellcheck="false" />
      <button type="button" onclick="submitFlag()">Verificar</button>
      <div id="flag-result"></div>
    </div>
    <div class="info">
      <h3>Hint</h3>
      <p>Las apariencias engañan. Analiza el archivo con las herramientas correctas y busca lo que se esconde dentro.</p>
    </div>
  </div>

  <script>
    function submitFlag() {
      var value = document.getElementById('flag-input').value.trim();
      var result = document.getElementById('flag-result');
      result.style.display = 'none';
      if (!value) return;

      fetch('/check_flag', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ flag: value })
      })
      .then(function(r) { return r.json(); })
      .then(function(d) {
        result.style.display = 'block';
        if (d.correct) {
          result.className = 'ok';
          result.innerHTML = '&#9989; Flag: <code style="color:#3fb950">' + d.real_flag + '</code>';
        } else {
          result.className = 'err';
          result.textContent = '✘ Flag incorrecta. Sigue analizando la imagen.';
        }
      })
      .catch(function() {
        result.className = 'err';
        result.style.display = 'block';
        result.textContent = 'Error de conexión al verificar.';
      });
    }

    document.getElementById('flag-input').addEventListener('keydown', function(e) {
      if (e.key === 'Enter') submitFlag();
    });
  </script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/check_flag', methods=['POST'])
def check_flag():
    data = request.get_json(silent=True) or {}
    submitted = (data.get('flag') or '').strip()
    if submitted == flag:
        return jsonify({'correct': True, 'real_flag': os.environ.get('FLAG')})
    return jsonify({'correct': False})

@app.route('/download/image')
def download_image():
    return send_file('/app/bajando_pepa.jpg', as_attachment=True, download_name='bajando_pepa.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)