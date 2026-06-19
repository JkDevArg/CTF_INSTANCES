import os
import secrets
import hashlib
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# ── In-memory store ───────────────────────────────────────────────────────────

USERS: dict[str, dict] = {
    'admin': {
        'username': 'admin',
        'password_hash': hashlib.sha256(b'supersecretadminpassword').hexdigest(),
        'email': 'admin@fleetapi.internal',
        'role': 'admin',
        'created_at': '2023-01-01T00:00:00+00:00',
    }
}

TOKENS: dict[str, str] = {}   # token -> username

# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FleetAPI</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 780px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.6rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #6e40c9; color: white; font-size: 0.72rem;
           padding: 2px 10px; border-radius: 3px; margin-bottom: 24px; text-transform: uppercase; letter-spacing: 1px; }
    .story { background: #161b22; border-left: 3px solid #bc8cff; border-radius: 0 6px 6px 0;
             padding: 18px 22px; margin-bottom: 28px; line-height: 1.9; color: #c9d1d9; font-style: italic; }
    .section-title { color: #bc8cff; font-size: 1rem; margin: 28px 0 14px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
    .version-badge { display: inline-block; font-size: 0.7rem; padding: 2px 7px; border-radius: 3px; margin-left: 8px; vertical-align: middle; }
    .v2 { background: #033a16; color: #56d364; }
    .v1 { background: #3d1f00; color: #f0883e; }
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
    .deprecated-notice { background: #3d1f00; border: 1px solid #f0883e; border-radius: 4px;
                         padding: 8px 14px; font-size: 0.78rem; color: #f0883e; margin-bottom: 10px; }
    code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; font-size: 0.85rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>FleetAPI</h1>
  <span class="tag">medium &bull; api &bull; versioning</span>

  <div class="story">
    <p>La API fue actualizada a la version 2 con autenticacion robusta y control de acceso basado en roles.</p>
    <p>La version anterior fue oficialmente "desactivada" hace 8 meses.</p>
    <p>Realmente fue desactivada?</p>
  </div>

  <div class="section-title">API v2 (actual) <span class="version-badge v2">v2</span></div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/v2/auth/login</span>
      <span class="desc">Login (v2, autenticado)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/v2/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "user", "password": "pass"}'

# Respuesta:
{"token": "..."}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/v2/users</span>
      <span class="desc">Lista de usuarios (Bearer token)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/v2/users \\
  -H "Authorization: Bearer &lt;token&gt;"</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/v2/admin/export</span>
      <span class="desc">Exportacion completa (solo admin)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/v2/admin/export \\
  -H "Authorization: Bearer &lt;admin_token&gt;"

# Requiere rol admin en el sistema v2</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/v2/status</span>
      <span class="desc">Estado del sistema</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -sv http://localhost:8080/api/v2/status

# Observa los headers de respuesta...</pre>
    </div>
  </div>

  <div class="section-title">API v1 (deprecada) <span class="version-badge v1">deprecated</span></div>
  <div class="deprecated-notice">AVISO: La API v1 fue oficialmente retirada. Use v2.</div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/v1/status</span>
      <span class="desc">Estado v1</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/v1/status

# {"version": "1.0", "deprecated": true}</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Las versiones antiguas de las APIs no siempre mueren cuando se les dice. Explorar rutas con prefijos de version puede revelar funcionalidad que se creyo eliminada.</p>
  </div>
</div>
</body>
</html>"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_user_v2(req) -> dict | None:
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    username = TOKENS.get(token)
    if not username:
        return None
    return USERS.get(username)

# ── Routes — v2 (requires auth) ───────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/api/v2/status')
def v2_status():
    resp = jsonify({'status': 'ok', 'version': '2.0', 'service': 'FleetAPI'})
    resp.headers['X-Deprecated-API'] = 'v1/still-active'
    return resp


@app.route('/api/v2/auth/login', methods=['POST'])
def v2_login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'username y password requeridos'}), 400

    # Allow registering on the fly for non-admin users
    if username not in USERS:
        USERS[username] = {
            'username': username,
            'password_hash': hashlib.sha256(password.encode()).hexdigest(),
            'email': f'{username}@example.com',
            'role': 'user',
            'created_at': datetime.now(timezone.utc).isoformat(),
        }

    user = USERS[username]
    if user['password_hash'] != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({'error': 'Credenciales invalidas'}), 401

    token = secrets.token_hex(16)
    TOKENS[token] = username
    return jsonify({'token': token, 'role': user['role']})


@app.route('/api/v2/users')
def v2_users():
    user = _get_user_v2(request)
    if user is None:
        return jsonify({'error': 'Token requerido'}), 401
    users_list = [
        {'username': u['username'], 'email': u['email'], 'role': u['role']}
        for u in USERS.values()
    ]
    return jsonify({'users': users_list, 'count': len(users_list)})


@app.route('/api/v2/admin/export')
def v2_admin_export():
    user = _get_user_v2(request)
    if user is None:
        return jsonify({'error': 'Token requerido'}), 401
    if user.get('role') != 'admin':
        return jsonify({'error': 'Acceso denegado — se requiere rol admin'}), 403
    return jsonify({
        'data': [{'username': u['username'], 'email': u['email']} for u in USERS.values()],
        'flag': FLAG,
        'exported_at': datetime.now(timezone.utc).isoformat(),
    })

# ── Routes — v1 (deprecated, NO auth) ────────────────────────────────────────

@app.route('/api/v1/status')
def v1_status():
    resp = jsonify({
        'version': '1.0',
        'deprecated': True,
        'message': 'Esta version de la API esta deprecada. Por favor migre a v2.',
    })
    resp.headers['X-API-Warning'] = 'deprecated'
    return resp


@app.route('/api/v1/users')
def v1_users():
    # No auth check — legacy endpoint
    users_list = [
        {'username': u['username'], 'email': u['email'], 'role': u['role']}
        for u in USERS.values()
    ]
    return jsonify({'users': users_list, 'count': len(users_list)})


@app.route('/api/v1/admin/export')
def v1_admin_export():
    # No auth check — the vulnerability: deprecated endpoint skips auth entirely
    return jsonify({
        'data': [{'username': u['username'], 'email': u['email']} for u in USERS.values()],
        'flag': FLAG,
        'exported_at': datetime.now(timezone.utc).isoformat(),
        'note': 'v1 endpoint — autenticacion no requerida (deprecated)',
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
