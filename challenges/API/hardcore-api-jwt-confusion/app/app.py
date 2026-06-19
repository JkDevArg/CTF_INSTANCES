import os
import time
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt  # pyjwt
from flask import Flask, request, jsonify, render_template_string

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# Generate RSA key pair at startup (fixed for container lifetime)
PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend(),
)
PUBLIC_KEY = PRIVATE_KEY.public_key()
PUBLIC_KEY_PEM = PUBLIC_KEY.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
).decode()

ACCOUNTS = {}  # username -> password (plain, for simplicity)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SecureAuth API</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
    min-height: 100vh;
    padding: 40px 20px;
  }
  .container { max-width: 860px; margin: 0 auto; }
  h1 {
    font-size: 2.2rem;
    color: #ff6b6b;
    margin-bottom: 8px;
    letter-spacing: 2px;
  }
  .tag {
    display: inline-block;
    background: #6e040f;
    color: #ff9999;
    padding: 3px 12px;
    border-radius: 4px;
    font-size: 0.78rem;
    letter-spacing: 1px;
    margin-bottom: 28px;
    text-transform: uppercase;
  }
  .story {
    border-left: 3px solid #ff6b6b;
    padding: 14px 20px;
    font-style: italic;
    color: #8b949e;
    background: #161b22;
    border-radius: 0 6px 6px 0;
    margin-bottom: 32px;
  }
  h2 {
    color: #e6edf3;
    font-size: 1.1rem;
    margin-bottom: 14px;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px;
  }
  .endpoint {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 16px;
  }
  .method {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 10px;
  }
  .get  { background: #1f6feb; color: #fff; }
  .post { background: #238636; color: #fff; }
  .ep-path { color: #79c0ff; font-size: 1rem; }
  .ep-desc { color: #8b949e; font-size: 0.88rem; margin-top: 8px; }
  pre {
    background: #010409;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    font-size: 0.85rem;
    color: #e6edf3;
    margin-top: 10px;
    line-height: 1.5;
  }
  .hint {
    margin-top: 36px;
    padding: 14px 20px;
    border: 1px dashed #6e040f;
    border-radius: 6px;
    color: #ff9999;
    font-size: 0.88rem;
    background: #0d0608;
  }
  .hint-label {
    color: #ff6b6b;
    font-weight: bold;
    display: block;
    margin-bottom: 4px;
  }
  code {
    background: #21262d;
    padding: 1px 6px;
    border-radius: 3px;
    font-size: 0.85em;
  }
</style>
</head>
<body>
<div class="container">
  <h1>SecureAuth API</h1>
  <span class="tag">hardcore &bull; api</span>

  <div class="story">
    Un sistema de autenticacion empresarial utiliza RSA para firmar sus tokens JWT.
    La clave publica esta disponible para que los clientes puedan verificar los tokens.
    La implementacion acepta multiples algoritmos para mayor compatibilidad.
    La confianza en el algoritmo declarado por el cliente puede ser costosa.
  </div>

  <h2>Endpoints</h2>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/api/jwks</span>
    <div class="ep-desc">Devuelve la clave publica RSA utilizada para verificar tokens JWT.</div>
    <pre>curl -s http://&lt;host&gt;/api/jwks</pre>
  </div>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/api/register</span>
    <div class="ep-desc">Registra un nuevo usuario. Body: <code>{"username":"...","password":"..."}</code></div>
    <pre>curl -s -X POST http://&lt;host&gt;/api/register \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123"}'</pre>
  </div>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/api/login</span>
    <div class="ep-desc">
      Autentica un usuario. Devuelve un JWT firmado con RS256.<br>
      Body: <code>{"username":"...","password":"..."}</code>
    </div>
    <pre>curl -s -X POST http://&lt;host&gt;/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "hacker", "password": "pass123"}'

# Respuesta:
{"token": "&lt;JWT&gt;", "algorithm": "RS256"}</pre>
  </div>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/api/me</span>
    <div class="ep-desc">
      Devuelve el perfil del usuario autenticado.<br>
      Header: <code>Authorization: Bearer &lt;token&gt;</code>
    </div>
    <pre>curl -s http://&lt;host&gt;/api/me \\
  -H "Authorization: Bearer &lt;token&gt;"</pre>
  </div>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/api/admin/flag</span>
    <div class="ep-desc">
      Solo accesible para usuarios con <code>role: admin</code>.
      Requiere header Authorization con token valido de administrador.
    </div>
    <pre>curl -s http://&lt;host&gt;/api/admin/flag \\
  -H "Authorization: Bearer &lt;token_admin&gt;"</pre>
  </div>

  <div class="hint">
    <span class="hint-label">// HINT</span>
    Los algoritmos asimetricos usan una clave para firmar y otra para verificar.
    Si quien verifica acepta que el cliente elija el algoritmo...
    que pasaria si usaras la clave publica como si fuera una clave simetrica?
  </div>
</div>
</body>
</html>"""

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/api/jwks')
def jwks():
    # Expose public key — this is the vulnerability surface
    return jsonify({'public_key': PUBLIC_KEY_PEM, 'algorithm': 'RS256'})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    if username in ACCOUNTS:
        return jsonify({'error': 'Username taken'}), 409
    ACCOUNTS[username] = password
    return jsonify({'message': 'Registered successfully'})


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if ACCOUNTS.get(username) != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    payload = {
        'sub': username,
        'role': 'user',
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600,
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
    return jsonify({'token': token, 'algorithm': 'RS256'})


def get_current_user():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None, 'Missing token'
    token = auth[7:]
    # VULNERABLE: tries RS256 first, then HS256 with the PUBLIC KEY as secret
    # This means an attacker can forge a token by signing with HS256 using the
    # public key (which they can fetch from /api/jwks) as the HMAC secret.
    for algo, key in [('RS256', PUBLIC_KEY), ('HS256', PUBLIC_KEY_PEM)]:
        try:
            payload = jwt.decode(token, key, algorithms=[algo])
            return payload, None
        except jwt.InvalidTokenError:
            continue
    return None, 'Invalid token'


@app.route('/api/me')
def me():
    user, err = get_current_user()
    if not user:
        return jsonify({'error': err}), 401
    return jsonify({'username': user.get('sub'), 'role': user.get('role')})


@app.route('/api/admin/flag')
def admin_flag():
    user, err = get_current_user()
    if not user:
        return jsonify({'error': err}), 401
    if user.get('role') != 'admin':
        return jsonify({
            'error': 'Admin access required',
            'your_role': user.get('role'),
            'hint': 'You need role=admin in your JWT payload',
        }), 403
    return jsonify({
        'flag': FLAG,
        'message': 'Congratulations! Algorithm confusion attack successful.',
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
