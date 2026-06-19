import os, jwt, json
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# Escribir claves de firma al iniciar
os.makedirs('/keys', exist_ok=True)
with open('/keys/default.key', 'w') as f:
    f.write(os.urandom(32).hex())

MAIN = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>AuthCorp JWT</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}pre{background:#001100;padding:12px;font-size:.85rem}.hint{color:#009920;font-style:italic}</style></head><body>
<h1>AuthCorp &mdash; JWT Authentication Service</h1>
<div class="box"><p>Servicio de autenticaci&oacute;n con JWT. Inicia sesi&oacute;n para obtener un token.</p></div>
<div class="box"><h2 style="color:#00cc33;margin-bottom:10px">API</h2>
<pre>POST /login   {"username":"user","password":"user123"}
GET  /profile  Authorization: Bearer &lt;jwt&gt;
GET  /admin    Authorization: Bearer &lt;jwt con role=admin&gt;</pre></div>
<div class="box"><p class="hint">La clave que firma el token depende de un par&aacute;metro que el usuario controla.</p></div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(MAIN)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    if data.get('username') == 'user' and data.get('password') == 'user123':
        payload = {'username': 'user', 'role': 'user'}
        token = jwt.encode(
            payload,
            open('/keys/default.key').read(),
            algorithm='HS256',
            headers={'kid': 'default'}
        )
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

def _load_key_for_token(token):
    """Carga el archivo de clave según el kid del header JWT — vulnerable a path traversal."""
    header = jwt.get_unverified_header(token)
    kid = header.get('kid', 'default')
    key_path = f'/keys/{kid}.key'
    try:
        return open(key_path).read()
    except FileNotFoundError:
        # Si el archivo no existe, clave vacía — ESTA ES LA VULNERABILIDAD
        return ''

@app.route('/profile')
def profile():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        key = _load_key_for_token(token)
        decoded = jwt.decode(token, key, algorithms=['HS256'])
        return jsonify({'user': decoded})
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/admin')
def admin():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        key = _load_key_for_token(token)
        decoded = jwt.decode(token, key, algorithms=['HS256'])
        if decoded.get('role') != 'admin':
            return jsonify({'error': 'Admin only'}), 403
        return jsonify({'flag': FLAG})
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
