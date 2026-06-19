import os
import secrets
import hashlib
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# ── In-memory user store ──────────────────────────────────────────────────────

USERS: dict[str, dict] = {}      # username -> user dict
TOKENS: dict[str, str] = {}      # token -> username

_uid = 0


def next_uid() -> int:
    global _uid
    _uid += 1
    return _uid

# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UserHub API</title>
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
    code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; font-size: 0.85rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>UserHub API</h1>
  <span class="tag">medium &bull; api &bull; mass assignment</span>

  <div class="story">
    <p>Una plataforma de registro de usuarios acepta datos JSON para crear cuentas.</p>
    <p>El backend es flexible con los campos que acepta del cliente.</p>
    <p>Quizas demasiado flexible.</p>
  </div>

  <div class="section-title">API Endpoints</div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/register</span>
      <span class="desc">Registra un nuevo usuario</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/register \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123", "email": "h@x.com"}'

# Respuesta:
{"token": "...", "message": "Cuenta creada"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/login</span>
      <span class="desc">Inicia sesion</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123"}'

# Respuesta:
{"token": "...", "message": "Login exitoso"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/profile</span>
      <span class="desc">Tu perfil (Bearer token requerido)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/profile \\
  -H "Authorization: Bearer &lt;token&gt;"

# Respuesta:
{"id": 1, "username": "hacker", "email": "h@x.com", "created_at": "..."}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/admin/dashboard</span>
      <span class="desc">Panel de administracion (solo admins)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/admin/dashboard \\
  -H "Authorization: Bearer &lt;token&gt;"

# Requiere cuenta con privilegios de administrador
# {"error": "Admin access required"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/users</span>
      <span class="desc">Lista de usuarios (solo admins)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/users \\
  -H "Authorization: Bearer &lt;token&gt;"</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Los frameworks modernos pueden ser generosos al parsear JSON. Si el backend no filtra los campos de entrada, el cliente puede definir mas de lo que deberia.</p>
  </div>
</div>
</body>
</html>"""

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()

    if not username or not password:
        return jsonify({'error': 'username y password requeridos'}), 400
    if username in USERS:
        return jsonify({'error': 'Usuario ya existe'}), 409

    # BUG: Mass assignment — build user from raw request data.
    # If the client sends "is_admin": true, it gets stored.
    user = {
        'id': next_uid(),
        'username': username,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
        'email': email,
        'is_admin': False,      # default: not admin
        'created_at': datetime.now(timezone.utc).isoformat(),
    }

    # Mass assignment: override defaults with whatever the client sent
    for key, value in data.items():
        if key in ('username', 'password', 'email'):
            continue   # already handled
        if key == 'password_hash':
            continue   # don't allow direct hash override
        user[key] = value   # <-- vulnerability: allows is_admin = true

    USERS[username] = user
    token = secrets.token_hex(16)
    TOKENS[token] = username

    return jsonify({'token': token, 'message': 'Cuenta creada'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'username y password requeridos'}), 400
    user = USERS.get(username)
    if not user:
        return jsonify({'error': 'Credenciales invalidas'}), 401
    if user['password_hash'] != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({'error': 'Credenciales invalidas'}), 401
    token = secrets.token_hex(16)
    TOKENS[token] = username
    return jsonify({'token': token, 'message': 'Login exitoso'})


def _get_user(req) -> dict | None:
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    username = TOKENS.get(token)
    if not username:
        return None
    return USERS.get(username)


@app.route('/api/profile')
def profile():
    user = _get_user(request)
    if user is None:
        return jsonify({'error': 'Token requerido o invalido'}), 401
    # Return profile — deliberately hiding is_admin to not hint at the field name
    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'created_at': user['created_at'],
    })


@app.route('/api/admin/dashboard')
def admin_dashboard():
    user = _get_user(request)
    if user is None:
        return jsonify({'error': 'Token requerido o invalido'}), 401
    if not user.get('is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403
    return jsonify({
        'message': 'Bienvenido al panel de administracion.',
        'flag': FLAG,
        'total_users': len(USERS),
    })


@app.route('/api/users')
def list_users():
    user = _get_user(request)
    if user is None:
        return jsonify({'error': 'Token requerido o invalido'}), 401
    if not user.get('is_admin', False):
        return jsonify({'error': 'Admin access required'}), 403
    users_list = [
        {'id': u['id'], 'username': u['username'], 'email': u['email']}
        for u in USERS.values()
    ]
    return jsonify({'users': users_list, 'count': len(users_list)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
