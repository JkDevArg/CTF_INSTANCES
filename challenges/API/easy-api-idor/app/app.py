import os
import sqlite3
import secrets
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

# ── In-memory SQLite ──────────────────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('''CREATE TABLE users (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        token   TEXT UNIQUE NOT NULL
    )''')
    conn.execute('''CREATE TABLE orders (
        id      INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        details TEXT NOT NULL
    )''')
    # Order #1 belongs to admin (user_id = 0) and contains the flag
    conn.execute("INSERT INTO orders VALUES (1, 0, ?)",
                 (f'PAQUETE CLASIFICADO — Contenido: {FLAG}',))
    # Decoy orders
    decoys = [
        (2, 0, 'Paquete estandar #2 — Camiseta talla M'),
        (3, 0, 'Paquete estandar #3 — Libro de Python'),
        (4, 0, 'Paquete estandar #4 — Auriculares inalambricos'),
        (5, 0, 'Paquete estandar #5 — Teclado mecanico'),
        (6, 0, 'Paquete estandar #6 — Monitor 24"'),
        (7, 0, 'Paquete estandar #7 — Webcam HD'),
        (8, 0, 'Paquete estandar #8 — Hub USB-C'),
        (9, 0, 'Paquete estandar #9 — SSD 1TB'),
    ]
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", decoys)
    conn.commit()
    return conn

DB = init_db()

# ── Token store: token -> user_id ────────────────────────────────────────────

TOKENS: dict[str, int] = {}

def get_user_from_token(req) -> int | None:
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    return TOKENS.get(token)

# ── HTML UI ───────────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PackTrack API</title>
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
  <h1>PackTrack API</h1>
  <span class="tag">easy &bull; api &bull; idor</span>

  <div class="story">
    <p>Un servicio de seguimiento de paquetes fue desplegado apresuradamente antes del Black Friday.</p>
    <p>Los desarrolladores asumieron que los usuarios solo consultarian sus propios pedidos.
       Nadie implemento una verificacion de propiedad en el backend.</p>
    <p>El pedido #1 es especial. Siempre lo fue.</p>
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
  -d '{"username": "hacker"}'

# Respuesta:
{"token": "a1b2c3d4e5f6...", "message": "Usuario registrado"}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/orders</span>
      <span class="desc">Lista tus pedidos (requiere token)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/orders \\
  -H "Authorization: Bearer &lt;token&gt;"

# Respuesta para usuario nuevo:
{"orders": [], "count": 0}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/orders/&lt;id&gt;</span>
      <span class="desc">Detalle de un pedido por ID (requiere token)</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/orders/102 \\
  -H "Authorization: Bearer &lt;token&gt;"

# Respuesta:
{"id": 102, "details": "Paquete estandar #102 — ..."}</pre>
    </div>
  </div>

  <div class="endpoint">
    <div class="endpoint-header">
      <span class="method get">GET</span>
      <span class="path">/api/profile</span>
      <span class="desc">Tu perfil de usuario</span>
    </div>
    <div class="endpoint-body">
      <pre>curl -s http://localhost:8080/api/profile \\
  -H "Authorization: Bearer &lt;token&gt;"</pre>
    </div>
  </div>

  <div class="hint">
    <div class="hint-title">// PISTA</div>
    <p>Los numeros secuenciales pueden revelar mas de lo esperado. El primer pedido de cualquier sistema suele ser el mas importante.</p>
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
    if not username:
        return jsonify({'error': 'username requerido'}), 400
    if len(username) > 32:
        return jsonify({'error': 'username demasiado largo'}), 400

    token = secrets.token_hex(16)
    try:
        cursor = DB.execute(
            "INSERT INTO users (username, token) VALUES (?, ?)", (username, token))
        DB.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Already exists — return existing token
        row = DB.execute("SELECT id, token FROM users WHERE username = ?", (username,)).fetchone()
        user_id, token = row['id'], row['token']

    TOKENS[token] = user_id
    return jsonify({'token': token, 'message': 'Usuario registrado', 'user_id': user_id}), 201


@app.route('/api/profile')
def profile():
    user_id = get_user_from_token(request)
    if user_id is None:
        return jsonify({'error': 'Token requerido'}), 401
    row = DB.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    if not row:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    orders_count = DB.execute(
        "SELECT COUNT(*) as c FROM orders WHERE user_id = ?", (user_id,)).fetchone()['c']
    return jsonify({'id': row['id'], 'username': row['username'], 'orders_count': orders_count})


@app.route('/api/orders')
def list_orders():
    user_id = get_user_from_token(request)
    if user_id is None:
        return jsonify({'error': 'Token requerido'}), 401
    rows = DB.execute(
        "SELECT id, details FROM orders WHERE user_id = ?", (user_id,)).fetchall()
    orders = [{'id': r['id'], 'details': r['details']} for r in rows]
    return jsonify({'orders': orders, 'count': len(orders)})


@app.route('/api/orders/<int:order_id>')
def get_order(order_id):
    # Authenticate user — but NEVER check ownership (IDOR vulnerability)
    user_id = get_user_from_token(request)
    if user_id is None:
        return jsonify({'error': 'Token requerido'}), 401

    row = DB.execute(
        "SELECT id, user_id, details FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not row:
        return jsonify({'error': 'Pedido no encontrado'}), 404

    # BUG: no ownership check — any authenticated user can see any order
    return jsonify({'id': row['id'], 'details': row['details']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
