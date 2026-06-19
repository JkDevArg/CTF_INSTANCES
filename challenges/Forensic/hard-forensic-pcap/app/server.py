from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>NetCapture Corp &mdash; HTTP Traffic Analysis</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', Courier, monospace; padding: 40px; }
  h1 { color: #00ff41; border-bottom: 1px solid #00ff41; padding-bottom: 12px; margin-bottom: 24px; font-size: 1.4rem; }
  h2 { color: #00cc33; margin-bottom: 12px; font-size: 1rem; }
  .box { border: 1px solid #003300; background: #050505; padding: 20px; margin-bottom: 20px; }
  a { color: #00ff41; }
  a:hover { color: #ffffff; }
  ul { padding-left: 20px; }
  li { margin-bottom: 8px; }
  .hint { color: #009920; font-style: italic; margin-top: 6px; }
  .tag { color: #ffaa00; font-size: 0.85rem; }
</style>
</head>
<body>
<h1>NetCapture Corp &mdash; HTTP Traffic Analysis</h1>

<div class="box">
  <h2>Descripci&oacute;n del reto</h2>
  <p>Se captur&oacute; tr&aacute;fico HTTP de la red interna de CorpSec durante un incidente de seguridad.</p>
  <p style="margin-top:10px;">La flag fue filtrada accidentalmente en <strong>dos peticiones distintas</strong>.</p>
  <p style="margin-top:10px;">Analiza el stream completo y reconstruye el secreto.</p>
</div>

<div class="box">
  <h2>Descargas</h2>
  <ul>
    <li><a href="/download/capture.log">capture.log &mdash; HTTP Stream Export (NetCapture Pro v2.3)</a></li>
    <li><a href="/download/README.txt">README.txt &mdash; Informaci&oacute;n del incidente</a></li>
  </ul>
</div>

<div class="box">
  <h2>Pistas t&eacute;cnicas</h2>
  <ul>
    <li>El archivo contiene <span class="tag">3 transacciones HTTP</span> completas (request + response).</li>
    <li>La flag est&aacute; dividida en <span class="tag">2 partes</span> — una en cada request/response diferente.</li>
    <li>Busca par&aacute;metros de URL y campos JSON en las respuestas.</li>
  </ul>
</div>

<div class="box">
  <p class="hint">El tr&aacute;fico nunca miente &mdash; pero hay que saber qu&eacute; buscar y d&oacute;nde mirar.</p>
</div>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('/app/dist', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
