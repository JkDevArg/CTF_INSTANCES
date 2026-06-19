import os
from flask import Flask, render_template_string

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>NovaCorp — Sitio Oficial</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
nav a{color:#00ff41;text-decoration:none;margin-right:20px}
nav a:hover{text-decoration:underline}
footer{color:#004400;margin-top:40px;font-size:0.85em;border-top:1px solid #002200;padding-top:15px}
.hint{color:#009920;font-style:italic}
</style></head>
<body>
<nav>[ <a href="/">Inicio</a> | <a href="/services">Servicios</a> | <a href="/blog">Blog</a> | <a href="/archive/">Archivo</a> | <a href="/contact">Contacto</a> ]</nav>
<br>
<h1>[ NovaCorp — Innovación Tecnológica ]</h1>
<div class="box">
  <h2>Bienvenido</h2>
  <p>NovaCorp es referente en soluciones de IA empresarial desde 2015.<br>
  Ayudamos a las empresas a transformar datos en decisiones.</p>
</div>
<div class="box">
  <h2>Noticias Recientes</h2>
  <p>▶ NovaCorp obtiene certificación SOC 2 Type II — Enero 2025</p>
  <p style="margin-top:8px">▶ Lanzamiento de NovaAI v5.0 — Diciembre 2024</p>
  <p style="margin-top:8px">▶ Expansión a mercado europeo — Noviembre 2024</p>
</div>
<footer>
  © 2025 NovaCorp S.A. &nbsp;|&nbsp;
  <a href="/archive/" style="color:#006600">Archivo histórico del sitio</a> (disponible para cumplimiento normativo)
</footer>
</body></html>"""

ARCHIVE_INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>NovaCorp — Archivo Histórico</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
.snapshot{border-bottom:1px solid #002200;padding:10px 0;display:flex;justify-content:space-between;align-items:center}
.snapshot:last-child{border-bottom:none}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.date{color:#009920}
.status{color:#006600;font-size:0.85em}
</style></head>
<body>
<h1>[ NovaCorp — Archivo Histórico del Sitio ]</h1>
<div class="box">
  <p>Este archivo contiene snapshots del sitio para cumplimiento normativo (GDPR, ISO 27001).<br>
  Las versiones antiguas se mantienen como registro histórico.</p>
</div>
<div class="box">
  <p style="color:#00cc33;margin-bottom:15px">Snapshots disponibles:</p>
  <div class="snapshot">
    <span><a href="/archive/2025-01/">Enero 2025</a></span>
    <span class="date">2025-01-01</span>
    <span class="status">[ACTUAL]</span>
  </div>
  <div class="snapshot">
    <span><a href="/archive/2024-11/">Noviembre 2024</a></span>
    <span class="date">2024-11-01</span>
    <span class="status">[archivado]</span>
  </div>
  <div class="snapshot">
    <span><a href="/archive/2024-07/">Julio 2024</a></span>
    <span class="date">2024-07-01</span>
    <span class="status">[archivado]</span>
  </div>
  <div class="snapshot">
    <span><a href="/archive/2024-01/">Enero 2024</a></span>
    <span class="date">2024-01-01</span>
    <span class="status">[archivado]</span>
  </div>
</div>
</body></html>"""

ARCHIVE_CURRENT = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[ARCHIVE 2025-01] NovaCorp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.archive-banner{background:#002200;border:1px solid #005500;padding:10px;margin-bottom:20px;color:#00aa00}</style></head>
<body>
<div class="archive-banner">[ARCHIVO] Snapshot: Enero 2025 — Versión archivada del sitio</div>
<h1>[ NovaCorp — Enero 2025 ]</h1>
<div class="box"><p>Versión archivada del sitio. Sin cambios significativos respecto a la versión actual.</p></div>
</body></html>"""

ARCHIVE_NOV = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[ARCHIVE 2024-11] NovaCorp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.archive-banner{background:#002200;border:1px solid #005500;padding:10px;margin-bottom:20px;color:#00aa00}</style></head>
<body>
<div class="archive-banner">[ARCHIVO] Snapshot: Noviembre 2024 — Versión archivada del sitio</div>
<h1>[ NovaCorp — Noviembre 2024 ]</h1>
<div class="box"><p>Lanzamiento de NovaAI v5.0 — revolucionando el análisis de datos empresariales.</p></div>
</body></html>"""

ARCHIVE_JULY = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[ARCHIVE 2024-07] NovaCorp</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.archive-banner{background:#002200;border:1px solid #005500;padding:10px;margin-bottom:20px;color:#00aa00}
nav a{color:#00ff41;text-decoration:none;margin-right:20px}
nav a:hover{text-decoration:underline}
</style></head>
<body>
<div class="archive-banner">[ARCHIVO] Snapshot: Julio 2024 — Versión archivada del sitio</div>
<nav>[ <a href="/archive/2024-07/">Inicio</a> | <a href="/archive/2024-07/announcements">Anuncios</a> | <a href="/archive/2024-07/api-docs">API Docs</a> ]</nav>
<br>
<h1>[ NovaCorp — Julio 2024 ]</h1>
<div class="box">
  <p>NovaCorp anuncia su plataforma NovaAI v4.0.<br>
  Integración con APIs externas disponible para partners.</p>
</div>
<div class="box">
  <p>Ver <a href="/archive/2024-07/announcements">anuncios internos de Julio 2024</a> para más detalles sobre la integración.</p>
</div>
</body></html>"""

OLD_ANNOUNCEMENT = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[ARCHIVE 2024-07] NovaCorp — Anuncios</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}}
.box{{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}}
h1{{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}}
.archive-banner{{background:#002200;border:1px solid #005500;padding:10px;margin-bottom:20px;color:#00aa00}}
.deleted{{color:#ff4141;font-size:0.85em}}
.api-key{{color:#00ff41;background:#001100;padding:10px;border:1px solid #003300;font-family:monospace;word-break:break-all;margin-top:10px}}
.warn{{color:#ffaa00}}
</style></head>
<body>
<div class="archive-banner">[ARCHIVO] Snapshot: Julio 2024 — Esta página fue eliminada del sitio en Agosto 2024</div>
<h1>[ NovaCorp — Anuncios Internos — Julio 2024 ]</h1>
<div class="box">
  <p style="color:#00cc33;margin-bottom:10px">Anuncio: Integración API v4.0 — Para Partners Certificados</p>
  <p>A partir del 1 de Agosto 2024, todos los partners deberán usar el nuevo endpoint de autenticación.</p>
  <p style="margin-top:10px">La clave de API de producción temporal asignada durante la migración:</p>
  <div class="api-key">{FLAG}</div>
  <p class="deleted" style="margin-top:10px">[NOTA: Esta página fue marcada para eliminación — API key comprometida, rotar inmediatamente]</p>
</div>
<div class="box">
  <p class="warn">[!] Este contenido fue "eliminado" del sitio actual pero permanece en el archivo histórico.</p>
</div>
</body></html>"""

ARCHIVE_JAN = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>[ARCHIVE 2024-01] NovaCorp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}.archive-banner{background:#002200;border:1px solid #005500;padding:10px;margin-bottom:20px;color:#00aa00}</style></head>
<body>
<div class="archive-banner">[ARCHIVO] Snapshot: Enero 2024 — Versión archivada del sitio</div>
<p style="padding:20px">Versión inicial del rediseño 2024. Sin contenido relevante.</p>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(INDEX)

@app.route('/archive/')
def archive_index():
    return render_template_string(ARCHIVE_INDEX)

@app.route('/archive/2025-01/')
def archive_jan25():
    return render_template_string(ARCHIVE_CURRENT)

@app.route('/archive/2024-11/')
def archive_nov():
    return render_template_string(ARCHIVE_NOV)

@app.route('/archive/2024-07/')
def archive_july():
    return render_template_string(ARCHIVE_JULY)

@app.route('/archive/2024-07/announcements')
def old_announcement():
    return render_template_string(OLD_ANNOUNCEMENT)

@app.route('/archive/2024-01/')
def archive_jan():
    return render_template_string(ARCHIVE_JAN)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
