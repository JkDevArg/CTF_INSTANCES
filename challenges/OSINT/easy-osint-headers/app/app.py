import os
from flask import Flask, render_template_string, jsonify, make_response

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>DataAPI Corp — Portal de API</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
code{background:#001100;padding:2px 6px;color:#00ff41}
.endpoint{margin:8px 0;padding:8px;border-left:2px solid #003300}
.hint{color:#009920;font-style:italic}
</style></head>
<body>
<h1>[ DataAPI Corp — Developer Portal ]</h1>
<div class="box">
  <p>Bienvenido al portal de desarrolladores de DataAPI Corp.<br>
  Documentación de endpoints disponibles abajo.</p>
</div>
<div class="box">
  <h2>Endpoints Públicos</h2>
  <div class="endpoint"><code>GET /api/status</code> — Estado del sistema</div>
  <div class="endpoint"><code>GET /api/version</code> — Versión de la API</div>
  <div class="endpoint"><code>GET /api/users/count</code> — Conteo de usuarios</div>
</div>
<div class="box">
  <h2>Nota de Seguridad</h2>
  <p>Todos los endpoints incluyen headers de diagnóstico interno.<br>
  <span class="hint">A veces la respuesta está en lo que el servidor no muestra en pantalla.</span></p>
</div>
</body></html>"""

def add_internal_headers(response):
    response.headers['X-Internal-Token'] = FLAG
    response.headers['X-API-Version'] = '4.2.1'
    response.headers['X-Server-Region'] = 'us-east-1-internal'
    response.headers['X-Build-Hash'] = 'a3f9c821'
    return response

@app.route('/')
def index():
    resp = make_response(render_template_string(INDEX))
    return add_internal_headers(resp)

@app.route('/api/status')
def api_status():
    resp = make_response(jsonify({
        "status": "operational",
        "uptime": "99.97%",
        "region": "us-east-1",
        "timestamp": "2024-01-15T09:42:00Z"
    }))
    return add_internal_headers(resp)

@app.route('/api/version')
def api_version():
    resp = make_response(jsonify({
        "version": "4.2.1",
        "build": "a3f9c821",
        "release": "stable",
        "deprecated": ["v1.x", "v2.x"]
    }))
    return add_internal_headers(resp)

@app.route('/api/users/count')
def users_count():
    resp = make_response(jsonify({
        "total_users": 48291,
        "active_today": 1847,
        "new_this_month": 392
    }))
    return add_internal_headers(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
