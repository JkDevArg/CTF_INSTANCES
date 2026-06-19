import os
import re
import secrets
from flask import Flask, request, jsonify, render_template_string

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# Simulated MongoDB-like document store
USERS_COLLECTION = [
    {
        "_id": "1",
        "username": "admin",
        "password": "s3cr3t_4dm1n_p4ss",
        "role": "admin",
        "secret": FLAG,
    },
    {
        "_id": "2",
        "username": "alice",
        "password": "alice2024",
        "role": "user",
        "secret": "nothing here",
    },
    {
        "_id": "3",
        "username": "bob",
        "password": "bob!123",
        "role": "user",
        "secret": "nothing here",
    },
]

SESSIONS = {}  # token -> _id


def mongo_match(doc, query):
    """Evaluate a MongoDB-style query against a document.
    Supports: $ne, $eq, $gt, $lt, $regex, $exists operators.
    """
    for field, condition in query.items():
        if field.startswith('$'):
            continue  # skip top-level logical operators
        value = doc.get(field)
        if isinstance(condition, dict):
            for op, operand in condition.items():
                if op == '$ne':
                    if not (value != operand):
                        return False
                elif op == '$eq':
                    if not (value == operand):
                        return False
                elif op == '$gt':
                    if not (str(value) > str(operand)):
                        return False
                elif op == '$lt':
                    if not (str(value) < str(operand)):
                        return False
                elif op == '$regex':
                    if not re.search(str(operand), str(value) if value else ''):
                        return False
                elif op == '$exists':
                    if bool(value is not None) != bool(operand):
                        return False
                # Unknown operators: silently ignore (another subtle bug)
        else:
            if value != condition:
                return False
    return True


def find_one(collection, query):
    for doc in collection:
        if mongo_match(doc, query):
            return doc
    return None


def find_all(collection, query):
    return [doc for doc in collection if mongo_match(doc, query)]


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DocStore API</title>
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
  <h1>DocStore API</h1>
  <span class="tag">hardcore &bull; api</span>

  <div class="story">
    Una API de almacenamiento de documentos usa MongoDB para persistencia.
    La capa de autenticacion parsea directamente el JSON de entrada y lo
    convierte en una consulta a la base de datos.
    La flexibilidad de NoSQL puede ser una ventaja... o una debilidad.
  </div>

  <h2>Endpoints</h2>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/api/login</span>
    <div class="ep-desc">
      Autentica un usuario con <code>username</code> y <code>password</code>.
      Devuelve un token de sesion.
    </div>
    <pre>curl -s -X POST http://&lt;host&gt;/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username": "alice", "password": "alice2024"}'

# Respuesta:
{"token": "...", "username": "alice", "role": "user"}</pre>
  </div>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/api/profile</span>
    <div class="ep-desc">
      Devuelve el perfil completo del usuario autenticado.<br>
      Header: <code>Authorization: Bearer &lt;token&gt;</code>
    </div>
    <pre>curl -s http://&lt;host&gt;/api/profile \\
  -H "Authorization: Bearer &lt;token&gt;"</pre>
  </div>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/api/search</span>
    <div class="ep-desc">
      Busca documentos de usuario. Acepta un objeto de filtro JSON.
      No requiere autenticacion.
    </div>
    <pre>curl -s -X POST http://&lt;host&gt;/api/search \\
  -H "Content-Type: application/json" \\
  -d '{"role": "user"}'

# Respuesta:
{"results": [...], "count": 2}</pre>
  </div>

  <div class="hint">
    <span class="hint-label">// HINT</span>
    Las bases de datos NoSQL a veces interpretan mas de lo que deberian
    cuando los valores son objetos en lugar de cadenas.
    MongoDB tiene operadores especiales que empiezan con <code>$</code>.
  </div>
</div>
</body>
</html>"""

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/api/login', methods=['POST'])
def login():
    # VULNERABLE: passes raw JSON directly to query — supports MongoDB operators
    data = request.get_json(silent=True)
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'username and password required'}), 400
    # Direct injection point: data['username'] and data['password'] can be
    # operator objects like {"$ne": ""} instead of plain strings
    query = {'username': data['username'], 'password': data['password']}
    user = find_one(USERS_COLLECTION, query)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = secrets.token_hex(16)
    SESSIONS[token] = user['_id']
    return jsonify({'token': token, 'username': user['username'], 'role': user['role']})


@app.route('/api/profile')
def profile():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return jsonify({'error': 'Authentication required'}), 401
    token = auth[7:]
    user_id = SESSIONS.get(token)
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401
    user = find_one(USERS_COLLECTION, {'_id': user_id})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Returns full profile including 'secret' field — but NOT the password
    return jsonify({k: v for k, v in user.items() if k != 'password'})


@app.route('/api/search', methods=['POST'])
def search():
    # Also vulnerable: allows searching with arbitrary MongoDB-style queries
    # No auth required — intended for "public" document search
    data = request.get_json(silent=True) or {}
    results = find_all(USERS_COLLECTION, data)
    # Strip password from results
    sanitized = [{k: v for k, v in doc.items() if k != 'password'} for doc in results]
    return jsonify({'results': sanitized, 'count': len(sanitized)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
