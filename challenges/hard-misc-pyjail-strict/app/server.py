from flask import Flask, render_template_string
app = Flask(__name__)

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>PyJail Corp — Sandbox v2.0 (Maximum Security)</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}a:hover{color:#fff}.hint{color:#009920;font-style:italic}h2{color:#00cc33;margin-bottom:10px;font-size:1rem}table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{border:1px solid #003300;padding:8px 14px;text-align:left}th{background:#001100;color:#00cc33}pre{background:#001100;padding:12px;overflow-x:auto;font-size:.85rem}</style></head><body>
<h1>PyJail Corp &mdash; Sandbox v2.0 (Maximum Security)</h1>
<div class="box"><h2>DESCRIPCION</h2><p>El sandbox de Python mas restrictivo que existe.<br><br>
<b>__builtins__ = {}</b> &mdash; absolutamente nada disponible. Ni print. Ni open. Ni dir. Ni getattr.<br><br>
La flag esta en <code>/home/ctf/flag.txt</code>.<br><br>
Conectate al puerto 9999 para interactuar con el jail.</p></div>
<div class="box"><h2>SANDBOX SETUP</h2><pre>SANDBOX = {'__builtins__': {}, '__name__': 'jail'}
result = eval(user_input, dict(SANDBOX))</pre></div>
<div class="box"><p class="hint">Sin herramientas, aun tienes el arbol. Sin builtins, aun tienes las clases.</p></div>
</body></html>"""

@app.route('/')
def index(): return render_template_string(PAGE)

if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
