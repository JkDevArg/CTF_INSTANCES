import os
from flask import Flask, send_file, render_template_string, request, jsonify

app = Flask(__name__)

flag = "H4L{RUST_VM_BYT3C0D3}"  # <-- reemplaza con la flag hardcodeada del reto

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>MateVM</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 680px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #1f6feb; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
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
    <h1>&#129302; MateVM</h1>
    <span class="tag">medium &bull; reversing</span>
    <p class="desc">
      Un desarrollador creó un sistema de verificación de licencias en Rust. Afirma que nadie puede
      romperlo porque no hay comparación directa de la flag.
      Demuéstrale que está equivocado.
    </p>
    <a href="/download" class="download-btn">&#11015; Download matevm</a>
    <div class="flag-form">
      <h3>&#127937; Ingresa la flag</h3>
      <input type="text" id="flag-input" placeholder="H4L{...}" autocomplete="off" spellcheck="false" />
      <button type="button" onclick="submitFlag()">Verificar</button>
      <div id="flag-result"></div>
    </div>
    <div class="info">
      <h3>Hint</h3>
      <p>La VM ejecuta un programa. Ese programa está cifrado. Descífralo y comprende sus instrucciones.</p>
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
          result.textContent = '✘ Flag incorrecta. Sigue analizando el binario.';
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
        return jsonify({'correct': True, 'real_flag': os.environ.get('FLAG', 'FLAG_NOT_CONFIGURED')})
    return jsonify({'correct': False})

@app.route('/download')
def download():
    return send_file('/app/matevm', as_attachment=True, download_name='matevm')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)