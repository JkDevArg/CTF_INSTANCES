import os
from flask import Flask, send_file, render_template_string, request, jsonify

app = Flask(__name__)

SECRET_ANSWER = "HL4{Th@nk$_t0_@ll_f0r_$upp0rt1nG}"

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Capas Ocultas</title>
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
    <h1>&#128269; Capas Ocultas</h1>
    <span class="tag">easy &bull; forensic</span>
    <p class="desc">
      Un archivo fue enviado como un simple ZIP. Pero las apariencias engañan.
      Cambia su extensión y mira con los ojos correctos.
    </p>
    <a href="/download" class="download-btn">&#11015; Download communities.zip</a>

    <div class="flag-form">
      <h3 style="color:#c9d1d9;font-size:0.95rem;margin-bottom:10px;">&#128275; Ingresa la clave oculta</h3>
      <input type="text" id="answer-input" placeholder="HL4{...}" autocomplete="off" />
      <button type="button" onclick="submitAnswer()">Verificar</button>
      <div id="flag-result"></div>
    </div>

    <div class="info">
      <h3>Hint</h3>
      <p>Las herramientas de diseño gráfico ven lo que los archivadores no pueden.</p>
    </div>
  </div>
  <script>
    function submitAnswer() {
      var answer = document.getElementById('answer-input').value.trim();
      var result = document.getElementById('flag-result');
      result.style.display = 'none';
      if (!answer) return;
      fetch('/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({answer: answer})
      })
      .then(function(r){ return r.json(); })
      .then(function(d){
        result.style.display = 'block';
        if (d.success) {
          result.className = 'ok';
          result.textContent = '&#9989; Flag: ' + d.flag;
          result.innerHTML = '&#9989; Flag: <code style="color:#3fb950">' + d.flag + '</code>';
        } else {
          result.className = 'err';
          result.textContent = '&#10060; ' + (d.message || 'Respuesta incorrecta');
        }
      })
      .catch(function(){ result.className='err'; result.style.display='block'; result.textContent='Error de conexión'; });
    }
    document.getElementById('answer-input').addEventListener('keydown', function(e){
      if (e.key === 'Enter') submitAnswer();
    });
  </script>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download')
def download():
    return send_file('/app/communities.zip', as_attachment=True, download_name='communities.zip')


@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json(silent=True) or {}
    answer = (data.get('answer') or '').strip()
    if answer == SECRET_ANSWER:
        flag = os.environ.get('FLAG', 'FLAG_NOT_CONFIGURED')
        return jsonify({'success': True, 'flag': flag})
    return jsonify({'success': False, 'message': 'Respuesta incorrecta'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
