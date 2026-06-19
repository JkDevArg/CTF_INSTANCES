import os
import secrets
import hashlib
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# ── In-memory user store ──────────────────────────────────────────────────────

USERS: dict[str, dict] = {}          # username -> user dict
TOKENS: dict[str, str] = {}          # token -> username

_uid_counter = 1


def next_uid() -> int:
    global _uid_counter
    uid = _uid_counter
    _uid_counter += 1
    return uid


# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DataVault API</title>
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
    code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; font-size: 0.85rem; }
  </style>
</head>
<body>
<div class="container">
  <h1>DataVault API</h1>
  <span class="tag">easy &bull; api &bull; data exposure</span>

  <div class="story">
    <p>Una plataforma de gestion de perfiles expone sus datos a traves de una API REST.</p>
    <p>El equipo de frontend solo muestra lo necesario: nombre de usuario y correo electronico.</p>
    <p>El backend, en cambio, devuelve todo lo que tiene. Todo.</p>
  </div>

  <div class="section-title">API Endpoints</div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/register</span>
      <span class="desc">Crea una cuenta nueva</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/register \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "email": "h@example.com", "password": "pass123"}'

# Respuesta (lo que el frontend muestra):
{"token": "...", "message": "Cuenta creada", "username": "hacker", "email": "h@example.com"}</pre>
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
      <span class="desc">Tu perfil de usuario (requiere token)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/profile \\
  -H "Authorization: Bearer &lt;token&gt;"

# El frontend muestra: username, email
# Pero la respuesta JSON tiene mas campos...</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Lo que no se muestra en pantalla no significa que no este ahi. Lee la respuesta JSON completa, no lo que el cliente decide renderizar.</p>
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
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not username or not email or not password:
        return jsonify({'error': 'username, email y password son requeridos'}), 400
    if username in USERS:
        return jsonify({'error': 'Usuario ya existe'}), 409

    token = secrets.token_hex(16)
    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    user = {
        'id': next_uid(),
        'username': username,
        'email': email,
        'password_hash': pw_hash,
        'role': 'user',
        'created_at': datetime.now(timezone.utc).isoformat(),
        'api_secret': FLAG,            # <-- excessive data exposure
        'internal_notes': 'Cuenta generada automaticamente por el sistema de registro.',
    }
    USERS[username] = user
    TOKENS[token] = username

    return jsonify({
        'token': token,
        'message': 'Cuenta creada',
        'username': username,
        'email': email,
    }), 201


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

    pw_hash = hashlib.sha256(password.encode()).hexdigest()
    if user['password_hash'] != pw_hash:
        return jsonify({'error': 'Credenciales invalidas'}), 401

    token = secrets.token_hex(16)
    TOKENS[token] = username
    return jsonify({'token': token, 'message': 'Login exitoso'})


@app.route('/api/profile')
def profile():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Token requerido'}), 401
    token = auth[7:]
    username = TOKENS.get(token)
    if not username:
        return jsonify({'error': 'Token invalido'}), 401

    user = USERS.get(username)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # BUG: returns the FULL user dict — including api_secret (the flag)
    # A proper implementation would whitelist only safe fields.
    return jsonify(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
