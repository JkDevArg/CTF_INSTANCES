from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AllocatorCorp &mdash; Note System</title>
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
<h1>AllocatorCorp &mdash; Note System</h1>

<div class="box">
  <h2>Servicio activo</h2>
  <p>Un sistema de gesti&oacute;n de notas corre en el puerto <strong>9999</strong>.</p>
  <p>Gestiona chunks en el heap. Algo en la l&oacute;gica de liberaci&oacute;n no es correcto.</p>
</div>

<div class="box">
  <h2>Descargas</h2>
  <ul style="padding-left:20px;">
    <li><a href="/download/allocator">allocator &mdash; ELF 64-bit x86-64</a></li>
  </ul>
</div>

<div class="box">
  <h2>Protecciones (checksec)</h2>
  <table>
    <tr><th>Protecci&oacute;n</th><th>Estado</th></tr>
    <tr><td>NX (No-Execute)</td>     <td class="ok">Enabled</td></tr>
    <tr><td>PIE</td>                 <td class="off">Disabled &mdash; direcci&oacute;n base fija</td></tr>
    <tr><td>Stack Canary</td>        <td class="off">Disabled</td></tr>
    <tr><td>RELRO</td>               <td class="off">Partial</td></tr>
    <tr><td>glibc</td>               <td class="ok">2.35 &mdash; tcache con protecci&oacute;n de clave</td></tr>
  </table>
</div>

<div class="box">
  <p class="hint">El heap nunca olvida lo que se libera &mdash; y lo que se libera dos veces revela sus secretos.</p>
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
