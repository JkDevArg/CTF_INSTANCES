import os
from flask import Flask, render_template_string, Response

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CorpSite — Tecnología Empresarial</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
nav a{color:#00ff41;text-decoration:none;margin-right:20px}
nav a:hover{text-decoration:underline}
.tag{background:#003300;color:#00ff41;padding:2px 8px;font-size:0.85em;margin-right:5px}
footer{color:#004400;margin-top:40px;font-size:0.85em}
</style></head>
<body>
<nav>[ <a href="/">Inicio</a> | <a href="/about">Nosotros</a> | <a href="/services">Servicios</a> | <a href="/contact">Contacto</a> ]</nav>
<br>
<h1>[ CorpSite — Soluciones Tecnológicas S.A. ]</h1>
<div class="box">
  <h2>Bienvenido a CorpSite</h2>
  <p>Somos líderes en soluciones tecnológicas empresariales desde 2008.<br>
  Nuestros servicios cubren infraestructura, ciberseguridad y transformación digital.</p>
</div>
<div class="box">
  <h2>Últimas Noticias</h2>
  <p><span class="tag">NUEVO</span> Lanzamos CorpSite Cloud v3.0 — migración sin interrupciones.</p>
  <p style="margin-top:10px"><span class="tag">SEC</span> Certificación ISO 27001 renovada para 2024-2025.</p>
  <p style="margin-top:10px"><span class="tag">CORP</span> Expansión a 5 nuevas ciudades en LATAM.</p>
</div>
<div class="box">
  <h2>Servicios</h2>
  <p>Infraestructura Cloud &bull; Seguridad Perimetral &bull; Auditoría TI &bull; Gestión de Identidades</p>
</div>
<footer>© 2024 CorpSite Soluciones Tecnológicas S.A. — Todos los derechos reservados.</footer>
</body></html>"""

ABOUT = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CorpSite — Nosotros</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}nav a{color:#00ff41;text-decoration:none;margin-right:20px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}</style></head>
<body>
<nav>[ <a href="/">Inicio</a> | <a href="/about">Nosotros</a> | <a href="/services">Servicios</a> | <a href="/contact">Contacto</a> ]</nav>
<br>
<h1>[ Sobre CorpSite ]</h1>
<div class="box">
  <p>CorpSite fue fundada en 2008 con la misión de digitalizar las empresas latinoamericanas.<br>
  Contamos con más de 500 clientes en 12 países y un equipo de 200 profesionales certificados.</p>
</div>
</body></html>"""

ROBOTS = """User-agent: *
Disallow: /admin/
Disallow: /admin/vault/
Disallow: /internal/
Disallow: /backup/
Disallow: /legacy/
"""

VAULT_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CorpSite — Vault</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #003300;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
.flag{color:#00ff41;font-size:1.2em;background:#001100;padding:15px;border:1px solid #00ff41;margin-top:15px;word-break:break-all}
.warn{color:#ffaa00}
</style></head>
<body>
<h1>[ /admin/vault/ — Acceso Interno ]</h1>
<div class="box">
  <p class="warn">[!] ÁREA RESTRINGIDA — Solo personal autorizado</p>
  <p style="margin-top:10px">Repositorio de credenciales y tokens de acceso interno.</p>
  <p style="margin-top:10px">Token de acceso corporativo:</p>
  <div class="flag">{{ flag }}</div>
</div>
<div class="box">
  <p style="color:#009920;font-style:italic">robots.txt fue diseñado para ocultar — no para proteger.</p>
</div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(INDEX)

@app.route('/about')
def about():
    return render_template_string(ABOUT)

@app.route('/robots.txt')
def robots():
    return Response(ROBOTS, mimetype='text/plain')

@app.route('/admin/')
def admin():
    return render_template_string("""<!DOCTYPE html><html><head><meta charset="utf-8"><title>403</title><style>body{background:#0a0a0a;color:#ff4141;font-family:'Courier New',monospace;padding:40px}</style></head><body><h1>[403] Forbidden</h1><p>Área administrativa — acceso denegado.</p></body></html>"""), 403

@app.route('/admin/vault/')
def vault():
    return render_template_string(VAULT_PAGE, flag=FLAG)

@app.route('/internal/')
def internal():
    return render_template_string("""<!DOCTYPE html><html><head><meta charset="utf-8"><title>403</title><style>body{background:#0a0a0a;color:#ff4141;font-family:'Courier New',monospace;padding:40px}</style></head><body><h1>[403] Forbidden</h1><p>Acceso denegado.</p></body></html>"""), 403

@app.route('/backup/')
def backup():
    return render_template_string("""<!DOCTYPE html><html><head><meta charset="utf-8"><title>403</title><style>body{background:#0a0a0a;color:#ff4141;font-family:'Courier New',monospace;padding:40px}</style></head><body><h1>[403] Forbidden</h1><p>Acceso denegado.</p></body></html>"""), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
