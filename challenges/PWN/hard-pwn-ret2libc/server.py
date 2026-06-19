from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>NetSec Corp &mdash; Data Processing Unit</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', Courier, monospace; padding: 40px; }
  h1 { color: #00ff41; border-bottom: 1px solid #00ff41; padding-bottom: 12px; margin-bottom: 24px; font-size: 1.4rem; }
  h2 { color: #00cc33; margin-bottom: 12px; font-size: 1rem; }
  .box { border: 1px solid #003300; background: #050505; padding: 20px; margin-bottom: 20px; }
  a { color: #00ff41; }
  a:hover { color: #ffffff; }
  table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
  th, td { border: 1px solid #003300; padding: 8px 14px; text-align: left; }
  th { background: #001100; color: #00cc33; }
  td.ok  { color: #00ff41; }
  td.off { color: #ff4444; }
  .hint { color: #009920; font-style: italic; margin-top: 6px; }
</style>
</head>
<body>
<h1>NetSec Corp &mdash; Data Processing Unit</h1>

<div class="box">
  <h2>Servicio activo</h2>
  <p>Un terminal de procesamiento de datos corre en el puerto <strong>9999</strong>.</p>
  <p>No hay funci&oacute;n ganadora. Deber&aacute;s construir tu propio camino hacia la shell.</p>
</div>

<div class="box">
  <h2>Descargas</h2>
  <ul style="padding-left:20px;">
    <li><a href="/download/target">target &mdash; ELF 64-bit x86-64</a></li>
    <li><a href="/download/libc.so.6">libc.so.6 &mdash; GNU C Library (Ubuntu 22.04)</a></li>
  </ul>
</div>

<div class="box">
  <h2>Protecciones (checksec)</h2>
  <table>
    <tr><th>Protecci&oacute;n</th><th>Estado</th></tr>
    <tr><td>NX (No-Execute)</td>     <td class="ok">Enabled</td></tr>
    <tr><td>PIE</td>                 <td class="off">Disabled &mdash; direcci&oacute;n base fija</td></tr>
    <tr><td>Stack Canary</td>        <td class="off">Disabled</td></tr>
    <tr><td>RELRO</td>               <td class="ok">Partial</td></tr>
  </table>
</div>

<div class="box">
  <p class="hint">Sin funci&oacute;n ganadora, el camino pasa por la libc &mdash; pero primero debes encontrarla.</p>
</div>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('/app/download', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
