import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MicroAPI</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 780px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.6rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #1f6feb; color: white; font-size: 0.72rem;
           padding: 2px 10px; border-radius: 3px; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 1px; }
    .story { background: #161b22; border-left: 3px solid #58a6ff; border-radius: 0 6px 6px 0;
             padding: 18px 22px; margin-bottom: 28px; line-height: 1.9; color: #c9d1d9; font-style: italic; }
    .section-title { color: #58a6ff; font-size: 1rem; margin: 28px 0 14px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
    .endpoint { background: #161b22; border: 1px solid #30363d; border-radius: 6px; margin-bottom: 14px; overflow: hidden; }
    .endpoint-header { display: flex; align-items: center; gap: 12px; padding: 12px 16px; }
    .method { font-size: 0.75rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; min-width: 50px; text-align: center; }
    .get  { background: #0d419d; color: #79c0ff; }
    .post { background: #033a16; color: #56d364; }
    .path { color: #e6edf3; font-size: 0.9rem; }
    .desc { color: #8b949e; font-size: 0.82rem; margin-left: auto; }
    .endpoint-body { border-top: 1px solid #21262d; padding: 14px 16px; }
    pre { background: #0d1117; border: 1px solid #21262d; border-radius: 4px;
          padding: 12px; font-size: 0.78rem; overflow-x: auto; color: #a5d6ff; line-height: 1.6; }
    .hint { background: #161b22; border: 1px solid #f0883e; border-radius: 6px;
            padding: 18px 22px; margin-top: 32px; }
    .hint-title { color: #f0883e; font-size: 0.85rem; margin-bottom: 8px; font-weight: bold; }
    .hint p { color: #8b949e; font-size: 0.85rem; line-height: 1.7; font-style: italic; }
    .notice { background: #161b22; border: 1px solid #30363d; border-radius: 6px;
              padding: 14px 18px; margin-bottom: 28px; font-size: 0.83rem; color: #8b949e; }
    .notice strong { color: #c9d1d9; }
    code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; font-size: 0.85rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>MicroAPI</h1>
  <span class="tag">easy &bull; api &bull; misconfiguration</span>

  <div class="story">
    <p>Una API minimalista fue disenada para uso interno de la infraestructura.</p>
    <p>Algunos endpoints no estan documentados. Solo son accesibles desde dentro de la red.</p>
    <p>La seguridad por oscuridad nunca fue suficiente.</p>
  </div>

  <div class="notice">
    <strong>Nota del sistema:</strong> Esta API tiene endpoints de configuracion interna solo accesibles
    desde dentro de la infraestructura. Los servicios externos solo pueden usar los endpoints publicos listados abajo.
  </div>

  <div class="section-title">API Endpoints (documentados)</div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/status</span>
      <span class="desc">Estado del servicio</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -sv http://localhost:8080/api/status

# Respuesta:
{"status": "ok", "version": "1.0", "service": "MicroAPI"}

# Nota: observa tambien las cabeceras de respuesta</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/docs</span>
      <span class="desc">Documentacion de endpoints</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/docs

# Respuesta:
{"endpoints": ["/api/status", "/api/users"], "version": "1.0"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/users</span>
      <span class="desc">Lista de usuarios registrados</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/users

# Respuesta:
{"users": [], "count": 0}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/debug/echo</span>
      <span class="desc">Eco de la solicitud (diagnostico)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/debug/echo \\
  -H "Content-Type: application/json" \\
  -d '{"test": "hello"}'

# Devuelve: body, headers y parametros de la peticion</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Las APIs internas a veces olvidan que el exterior puede llamarlas tambien. Un simple encabezado puede ser la llave que abre la puerta.</p>
  </div>
</div>
</body>
</html>"""

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/api/status')
def status():
    resp = jsonify({'status': 'ok', 'version': '1.0', 'service': 'MicroAPI'})
    resp.headers['X-Powered-By'] = 'InternalAPI/1.0'
    return resp


@app.route('/api/docs')
def docs():
    return jsonify({'endpoints': ['/api/status', '/api/users'], 'version': '1.0'})


@app.route('/api/users')
def users():
    return jsonify({'users': [], 'count': 0})


@app.route('/api/debug/echo', methods=['POST'])
def echo():
    body = request.get_json(silent=True) or {}
    headers_dict = {k: v for k, v in request.headers if k.startswith('X-') or k in ('Content-Type', 'Accept')}
    return jsonify({
        'echo': {
            'body': body,
            'headers': headers_dict,
            'method': request.method,
            'path': request.path,
        }
    })


@app.route('/api/internal/config')
def internal_config():
    # "Security": only allow requests that include the internal header
    # This is NOT real security — anyone can add a header
    internal = request.headers.get('X-Internal-Request', '')
    if internal.lower() != 'true':
        return jsonify({
            'error': 'Forbidden',
            'message': 'Este endpoint es solo para uso interno',
        }), 403

    return jsonify({
        'config': {
            'service': 'MicroAPI',
            'env': 'production',
            'debug': False,
            'internal_key': FLAG,
        }
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'error': 'Not found',
        'hint': 'Some routes are only for internal services',
    }), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
