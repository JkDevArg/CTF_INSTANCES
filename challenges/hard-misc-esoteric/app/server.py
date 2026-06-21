from flask import Flask, send_from_directory, render_template_string
app = Flask(__name__)

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Signal Corps — Classified Transmission</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}a:hover{color:#fff}.hint{color:#009920;font-style:italic}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{border:1px solid #003300;padding:8px 14px;text-align:left}th{background:#001100;color:#00cc33}pre{background:#001100;padding:12px;overflow-x:auto;font-size:.85rem}</style></head><body>
<h1>Signal Corps &mdash; Classified Transmission</h1>
<div class="box"><h2>MISION</h2><p>Se intercepto una transmision clasificada. Parece codificada en multiples capas.<br><br>
Descifra capa por capa para llegar al mensaje original.<br><br>
El orden de decodificacion importa. La ultima capa aplicada es la primera a revertir.</p></div>
<div class="box"><h2>ARCHIVOS</h2>
<p><a href="/download/transmission.txt">transmission.txt</a> &mdash; La transmision interceptada</p>
<p><a href="/download/bf.py">bf.py</a> &mdash; Interprete auxiliar (puede ser util)</p>
</div>
<div class="box"><p class="hint">Tres velos cubren la verdad. El primero gira, el segundo habla en puntos, el tercero en cuatro digitos.</p></div>
</body></html>"""

@app.route('/')
def index(): return render_template_string(PAGE)

@app.route('/download/<path:f>')
def download(f): return send_from_directory('/app/dist', f, as_attachment=True)

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
