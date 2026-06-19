import os
import hashlib
import datetime
from flask import Flask, request, jsonify, render_template_string

try:
    import jwt
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyjwt'])
    import jwt

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

JWT_SECRET = "hackl4bs"   # weak, dictionary-crackable secret
JWT_ALGORITHM = "HS256"

# ── In-memory user store ──────────────────────────────────────────────────────

USERS: dict[str, dict] = {}   # username -> {username, password_hash}


def make_token(username: str, role: str = "user") -> str:
    payload = {
        "sub": username,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_token_from_request() -> str | None:
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        return auth[7:]
    return None

# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AuthCore API</title>
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
  <h1>AuthCore API</h1>
  <span class="tag">medium &bull; api &bull; jwt</span>

  <div class="story">
    <p>Un sistema de autenticacion basado en JWT protege el acceso a los recursos.</p>
    <p>Los tokens firmados garantizan la integridad del payload. El rol esta embebido en el token.</p>
    <p>Pero, que tan fuerte es la firma?</p>
  </div>

  <div class="section-title">API Endpoints</div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/register</span>
      <span class="desc">Crea una cuenta</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/register \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123"}'

# Respuesta:
{"message": "Usuario registrado exitosamente"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method post">POST</span>
      <span class="path">/api/login</span>
      <span class="desc">Obtiene un JWT</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s -X POST http://localhost:8080/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123"}'

# Respuesta:
{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/me</span>
      <span class="desc">Tu informacion de usuario (Bearer JWT)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/me \\
  -H "Authorization: Bearer &lt;token&gt;"

# Respuesta:
{"username": "hacker", "role": "user"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/auth/info</span>
      <span class="desc">Informacion del sistema de autenticacion</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/auth/info

# Respuesta:
{"algorithm": "HS256", "token_example": "eyJ..."}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/admin/flag</span>
      <span class="desc">Solo administradores (role: admin)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/admin/flag \\
  -H "Authorization: Bearer &lt;admin_token&gt;"

# Requiere: {"role": "admin"} en el payload del JWT</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/admin/users</span>
      <span class="desc">Lista de usuarios (solo admin)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/admin/users \\
  -H "Authorization: Bearer &lt;admin_token&gt;"</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Un secreto predecible convierte la firma en una ilusion de seguridad. Las herramientas de cracking de JWT conocen los secretos mas comunes.</p>
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
    if not username or not password:
        return jsonify({'error': 'username y password requeridos'}), 400
    if username in USERS:
        return jsonify({'error': 'Usuario ya existe'}), 409
    USERS[username] = {
        'username': username,
        'password_hash': hashlib.sha256(password.encode()).hexdigest(),
    }
    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


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
    token = make_token(username, role='user')
    return jsonify({'token': token})


@app.route('/api/me')
def me():
    raw = get_token_from_request()
    if not raw:
        return jsonify({'error': 'Token requerido'}), 401
    payload = decode_token(raw)
    if not payload:
        return jsonify({'error': 'Token invalido o expirado'}), 401
    return jsonify({'username': payload.get('sub'), 'role': payload.get('role')})


@app.route('/api/auth/info')
def auth_info():
    # Give the player a real signed token to analyze
    example_token = make_token('demo_user', role='user')
    return jsonify({
        'algorithm': JWT_ALGORITHM,
        'token_example': example_token,
        'note': 'Los tokens son HMAC-SHA256. El payload contiene sub y role.',
    })


@app.route('/api/admin/flag')
def admin_flag():
    raw = get_token_from_request()
    if not raw:
        return jsonify({'error': 'Token requerido'}), 401
    payload = decode_token(raw)
    if not payload:
        return jsonify({'error': 'Token invalido o expirado'}), 401
    if payload.get('role') != 'admin':
        return jsonify({'error': 'Acceso denegado — se requiere rol admin'}), 403
    return jsonify({'flag': FLAG, 'message': 'Bienvenido, administrador.'})


@app.route('/api/admin/users')
def admin_users():
    raw = get_token_from_request()
    if not raw:
        return jsonify({'error': 'Token requerido'}), 401
    payload = decode_token(raw)
    if not payload:
        return jsonify({'error': 'Token invalido o expirado'}), 401
    if payload.get('role') != 'admin':
        return jsonify({'error': 'Acceso denegado — se requiere rol admin'}), 403
    users_list = [{'username': u} for u in USERS]
    return jsonify({'users': users_list, 'count': len(users_list)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
