from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>HEAP Corp — Note Manager</title>
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
  .hint { color: #009920; font-style: italic; }
  code { background: #001100; padding: 2px 6px; border-radius: 3px; font-size: 0.85rem; }
  .struct { font-size: 0.85rem; line-height: 1.6; }
</style>
</head>
<body>
<h1>HEAP Corp &mdash; Note Manager v0.1</h1>

<div class="box">
  <h2>Servicio activo</h2>
  <p>Un gestor de notas basado en heap corre en el puerto <strong>9999</strong>.</p>
  <p>Puedes crear, eliminar, leer y editar notas. Algo en el ciclo de vida no es correcto.</p>
</div>

<div class="box">
  <h2>Descargas</h2>
  <ul style="padding-left:20px;">
    <li><a href="/download/notectl">notectl &mdash; ELF 64-bit x86-64</a></li>
  </ul>
</div>

<div class="box">
  <h2>Estructura de datos</h2>
  <pre class="struct">typedef struct {
    void (*fn)(void);   // puntero a funci&oacute;n [offset 0, 8 bytes]
    char  msg[56];      // mensaje               [offset 8, 56 bytes]
} Note;                 // sizeof(Note) == 64</pre>
</div>

<div class="box">
  <h2>Protecciones (checksec)</h2>
  <table>
    <tr><th>Protecci&oacute;n</th><th>Estado</th></tr>
    <tr><td>NX (No-Execute)</td>     <td class="ok">Enabled</td></tr>
    <tr><td>PIE</td>                 <td class="off">Disabled &mdash; direcciones est&aacute;ticas</td></tr>
    <tr><td>Stack Canary</td>        <td class="off">Disabled</td></tr>
    <tr><td>RELRO</td>               <td class="ok">Partial</td></tr>
  </table>
</div>

<div class="box">
  <p class="hint">La memoria olvidada no desaparece &mdash; solo cambia de due&ntilde;o.</p>
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
