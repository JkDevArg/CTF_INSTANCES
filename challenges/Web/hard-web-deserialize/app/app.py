import os, pickle, base64
from flask import Flask, request, render_template_string, make_response, redirect

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

with open('/flag.txt', 'w') as f:
    f.write(FLAG + '\n')

class UserSession:
    def __init__(self, username, role='user'):
        self.username = username
        self.role = role

def load_session(cookie_b64):
    try:
        data = base64.b64decode(cookie_b64)
        return pickle.loads(data)  # VULNERABLE
    except:
        return None

def save_session(session_obj):
    return base64.b64encode(pickle.dumps(session_obj)).decode()

INDEX = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>PickleCorp Portal</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}input{background:#001100;color:#00ff41;border:1px solid #003300;padding:8px;font-family:'Courier New',monospace;width:200px}button{background:#003300;color:#00ff41;border:1px solid #00ff41;padding:8px 20px;cursor:pointer;font-family:'Courier New',monospace}.hint{color:#009920;font-style:italic}</style></head><body>
<h1>PickleCorp &mdash; Portal de Empleados</h1>
<div class="box"><p>Bienvenido. Inicia sesi&oacute;n para acceder al portal.</p></div>
<div class="box">
<form method="POST" action="/login">
<label>Usuario: <input name="username" value="guest"></label><br><br>
<button type="submit">Iniciar sesi&oacute;n</button>
</form></div>
<div class="box"><p class="hint">Tu sesi&oacute;n viaja contigo &mdash; dentro de una cookie serializada.</p></div>
</body></html>"""

DASHBOARD = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>PickleCorp Dashboard</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}.admin{color:#ff4444}.hint{color:#009920;font-style:italic}</style></head><body>
<h1>Dashboard</h1>
<div class="box"><p>Bienvenido, <strong>{{username}}</strong> (rol: <strong>{{role}}</strong>)</p></div>
{% if role == 'admin' %}
<div class="box"><p class="admin">[ADMIN] Flag: {{flag}}</p></div>
{% else %}
<div class="box"><p>No tienes permisos de administrador.</p></div>
{% endif %}
<div class="box"><p class="hint">Los datos del administrador est&aacute;n reservados para el rol correcto.</p></div>
</body></html>"""

@app.route('/')
def index():
    cookie = request.cookies.get('session')
    if cookie:
        session = load_session(cookie)
        if session:
            return render_template_string(DASHBOARD,
                username=getattr(session, 'username', '?'),
                role=getattr(session, 'role', 'user'),
                flag=FLAG)
    return render_template_string(INDEX)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', 'guest')
    session = UserSession(username, role='user')
    resp = make_response(redirect('/'))
    resp.set_cookie('session', save_session(session))
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
