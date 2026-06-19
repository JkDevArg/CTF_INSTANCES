import os
from flask import Flask, render_template_string

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>TechLeaks — Noticias de Ciberseguridad</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
.article{border-bottom:1px solid #002200;padding:15px 0}
.article:last-child{border-bottom:none}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.tag{background:#003300;color:#00cc33;padding:2px 8px;font-size:0.8em}
.date{color:#006600;font-size:0.85em}
.hint{color:#009920;font-style:italic}
</style></head>
<body>
<h1>[ TechLeaks — Noticias de Ciberseguridad ]</h1>
<div class="box">
  <div class="article">
    <p class="date">2024-01-15</p>
    <h2><a href="/blog/post/leaked-config">CorpCorp S.A.: Documento Interno Filtrado en GitHub</a></h2>
    <p style="margin-top:8px"><span class="tag">EXCLUSIVA</span> Un repositorio de GitHub de CorpCorp expone accidentalmente configuración interna. Según fuentes anónimas, el token fue publicado en un paste externo antes de ser eliminado.</p>
  </div>
  <div class="article">
    <p class="date">2024-01-12</p>
    <h2>Vulnerabilidad crítica en sistemas bancarios latinoamericanos</h2>
    <p style="margin-top:8px">Investigadores descubren fallo de inyección SQL en plataformas de 3 bancos regionales...</p>
  </div>
  <div class="article">
    <p class="date">2024-01-10</p>
    <h2>Ransomware RiftLock golpea infraestructura crítica en Chile</h2>
    <p style="margin-top:8px">El grupo RiftLock reivindica ataque a operadoras de telecomunicaciones...</p>
  </div>
</div>
<div class="box">
  <p class="hint">Cada pista lleva a la siguiente — sigue la cadena.</p>
</div>
</body></html>"""

BLOG_POST = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CorpCorp — Documento Interno Filtrado | TechLeaks</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.meta{color:#006600;font-size:0.85em;margin-bottom:15px}
.excerpt{border-left:3px solid #003300;padding-left:15px;color:#00cc33;margin:15px 0}
.hint{color:#009920;font-style:italic}
nav{margin-bottom:20px}
</style></head>
<body>
<nav><a href="/">← TechLeaks</a></nav>
<h1>[ CorpCorp S.A.: Documento Interno Filtrado en GitHub ]</h1>
<div class="box">
  <p class="meta">Autor: r3dteam_reporter &nbsp;|&nbsp; Publicado: 2024-01-15 &nbsp;|&nbsp; Categoría: OSINT, Filtraciones</p>
  <p>Un repositorio en el perfil de GitHub de CorpCorp contiene historial de commits que revela credenciales eliminadas.</p>
  <p style="margin-top:12px">Según el análisis del repositorio <strong>corpcorp/configs</strong>, un commit reciente intentó eliminar referencias a un token de producción. El commit message menciona explícitamente la URL de un paste externo donde el token fue publicado.</p>
  <div class="excerpt">
    "Nuestras fuentes confirman que el repositorio sigue siendo público. El historial de commits no miente — aunque el archivo sea eliminado, el mensaje permanece."
  </div>
  <p>Para reproducir el hallazgo, accede directamente al repositorio:</p>
  <p style="margin-top:10px"><a href="/github/corpcorp/configs">→ Ver repositorio corpcorp/configs en GitHub</a></p>
</div>
<div class="box">
  <p class="hint">El pasado no se borra — solo se entierra.</p>
</div>
</body></html>"""

GITHUB_REPO = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>corpcorp/configs — GitHub</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#c9d1d9;font-family:'Courier New',monospace;padding:0}
.header{background:#161b22;padding:16px 40px;border-bottom:1px solid #30363d;color:#58a6ff}
.main{padding:40px;max-width:1000px;margin:0 auto}
.repo-header{margin-bottom:20px}
.repo-name{font-size:1.4em;color:#58a6ff}
.tabs{border-bottom:1px solid #30363d;margin-bottom:20px;padding-bottom:0}
.tab{display:inline-block;padding:8px 16px;color:#8b949e;cursor:pointer}
.tab.active{color:#f0f6fc;border-bottom:2px solid #f78166}
.commits-header{color:#8b949e;font-size:0.9em;margin-bottom:15px}
.commit{border:1px solid #30363d;border-radius:6px;padding:12px 16px;margin-bottom:10px;background:#161b22}
.commit-msg{color:#e6edf3;font-size:1em}
.commit-msg a{color:#58a6ff;text-decoration:none}
.commit-msg a:hover{text-decoration:underline}
.commit-meta{color:#8b949e;font-size:0.85em;margin-top:6px}
.commit-hash{font-family:monospace;color:#8b949e;font-size:0.85em}
.badge-red{background:#da3633;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.8em}
.badge-green{background:#238636;color:#fff;padding:2px 8px;border-radius:12px;font-size:0.8em}
</style></head>
<body>
<div class="header">GitHub &mdash; corpcorp / configs</div>
<div class="main">
  <div class="repo-header">
    <div class="repo-name">&#128193; corpcorp / configs <span style="color:#8b949e;font-size:0.8em">[Public]</span></div>
    <div style="color:#8b949e;margin-top:6px">Repositorio de configuraciones internas de infraestructura</div>
  </div>
  <div class="tabs">
    <span class="tab">Code</span>
    <span class="tab active">Commits (7)</span>
    <span class="tab">Issues</span>
    <span class="tab">Settings</span>
  </div>
  <div class="commits-header">7 commits en branch main</div>

  <div class="commit">
    <div class="commit-msg"><span class="badge-red">URGENTE</span> Remove token from paste: /paste/abc123 — token comprometido, revocar acceso</div>
    <div class="commit-meta">sysadmin_corp · <span class="commit-hash">a1b2c3d</span> · 2024-01-14 23:47</div>
  </div>

  <div class="commit">
    <div class="commit-msg">Update production config — rotate API keys Q1 2024</div>
    <div class="commit-meta">devops_cc · <span class="commit-hash">e4f5g6h</span> · 2024-01-14 21:30</div>
  </div>

  <div class="commit">
    <div class="commit-msg">Add nginx config for corpcorp-api.local</div>
    <div class="commit-meta">infra_team · <span class="commit-hash">i7j8k9l</span> · 2024-01-10 14:22</div>
  </div>

  <div class="commit">
    <div class="commit-msg"><span class="badge-green">INIT</span> Initial commit — infrastructure configs</div>
    <div class="commit-meta">sysadmin_corp · <span class="commit-hash">m0n1o2p</span> · 2024-01-01 09:00</div>
  </div>
</div>
</body></html>"""

PASTE_404 = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>PasteBin Corp — 404</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}</style></head>
<body><h1>[404] Paste no encontrado</h1><p>Este paste ha expirado o fue eliminado.</p></body></html>"""


@app.route('/')
def index():
    return render_template_string(INDEX)


@app.route('/blog/post/leaked-config')
def blog_post():
    return render_template_string(BLOG_POST)


@app.route('/github/corpcorp/configs')
def github_repo():
    return render_template_string(GITHUB_REPO)


@app.route('/paste/abc123')
def paste():
    flag_hex = FLAG.encode().hex()
    PASTE_PAGE = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>PasteBin Corp — abc123</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}}
h1{{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}}
.box{{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}}
.meta{{color:#006600;font-size:0.85em;margin-bottom:15px}}
.content{{background:#001100;border:1px solid #003300;padding:15px;font-family:monospace;word-break:break-all;color:#00ff41}}
.label{{color:#00cc33;margin-bottom:8px}}
.hint{{color:#009920;font-style:italic}}
</style></head>
<body>
<h1>[ PasteBin Corp — Paste: abc123 ]</h1>
<div class="box">
  <div class="meta">Autor: anon_drop &nbsp;|&nbsp; Creado: 2024-01-14 23:15 &nbsp;|&nbsp; Vistas: 1 &nbsp;|&nbsp; <span style="color:#ff4141">PRIVADO</span></div>
  <div class="label">Token de producción CorpCorp (hex encoded):</div>
  <div class="content">{flag_hex}</div>
</div>
<div class="box">
  <p class="hint">hex → bytes → string. La decodificación es el último paso.</p>
</div>
</body></html>"""
    return render_template_string(PASTE_PAGE)


@app.route('/paste/<paste_id>')
def paste_generic(paste_id):
    return render_template_string(PASTE_404), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
