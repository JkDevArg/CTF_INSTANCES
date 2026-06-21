import os
from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>ScaryNet — Archivo Digital</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41}
.hint{color:#009920;font-style:italic}
p{line-height:1.7}
</style></head><body>
<h1>ScaryNet &mdash; Archivo de Pesadillas Digitales</h1>
<div class="box">
<p>He intentado borrar los peores recuerdos de internet de mi cabeza, pero es in&uacute;til.<br>
Cada noche, un desfile de pesadillas digitales pasa ante mis ojos.<br>
Trato de no darle importancia, pero hay una silueta que pesa en mi mente mucho m&aacute;s que las dem&aacute;s.<br><br>
&iquest;Podr&aacute;s aislarla y descubrir qu&eacute; oculta?</p>
</div>
<div class="box">
<h2 style="color:#00cc33;margin-bottom:10px">Archivo</h2>
<ul style="padding-left:20px">
<li><a href="/download/scary.gif">scary.gif &mdash; Animaci&oacute;n capturada de la red</a></li>
</ul>
</div>
<div class="box"><p class="hint">No todo tiene el mismo peso &mdash; y el bit m&aacute;s peque&ntilde;o guarda el secreto m&aacute;s grande.</p></div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory('/app/static', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
