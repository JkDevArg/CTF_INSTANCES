import os
import base64
import codecs
from flask import Flask, render_template_string

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

def get_encoded_flag():
    # Encode: base64 first, then rot13
    b64 = base64.b64encode(FLAG.encode()).decode()
    rot = codecs.encode(b64, 'rot13')
    return rot

NEWS_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CipherNews — Whistleblower Alex Turing</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
.article{padding:20px 0}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.meta{color:#006600;font-size:0.85em;margin-bottom:12px}
.excerpt{border-left:3px solid #003300;padding-left:15px;color:#00cc33;margin:15px 0;font-style:italic}
.tag{background:#003300;color:#00cc33;padding:2px 8px;font-size:0.8em;margin-right:5px}
.hint{color:#009920;font-style:italic}
</style></head>
<body>
<h1>[ CipherNews — Periodismo de Investigación ]</h1>
<div class="box">
  <div class="article">
    <p class="meta">
      <span class="tag">EXCLUSIVA</span>
      <span class="tag">WHISTLEBLOWER</span>
      2024-01-20 &nbsp;|&nbsp; Por: investigacion@ciphernews.local
    </p>
    <h2>Alex Turing: el informante que expuso las operaciones de CorpCorp</h2>
    <p>Un ingeniero de software que trabajó durante 4 años en CorpCorp S.A. decidió exponer las prácticas irregulares de la empresa. Conocido solo como "Alex Turing", el informante ha mantenido un perfil digital cuidadosamente construido a través de múltiples plataformas.</p>
    <div class="excerpt">
      "Encontramos su perfil público en LinkedIn bajo el nombre Alex Turing. Desde ahí, la cadena de evidencia digital nos llevó por un camino sorprendente."
    </div>
    <p>Investiga el rastro digital de Alex Turing empezando por su perfil profesional:</p>
    <p style="margin-top:10px"><a href="/linkedin/alex-turing">→ Ver perfil LinkedIn de Alex Turing</a></p>
  </div>
</div>
<div class="box">
  <p class="hint">Cinco pasos separan la noticia del secreto — cada plataforma es un paso.</p>
</div>
</body></html>"""

LINKEDIN_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Alex Turing — LinkedIn</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1d2226;color:#ffffff;font-family:'Courier New',monospace;padding:0}
.header{background:#283e4a;padding:16px 40px;border-bottom:1px solid #38434f;color:#0a66c2;font-size:1.2em}
.main{padding:0;max-width:800px;margin:0 auto}
.cover{background:linear-gradient(135deg,#0a66c2,#004182);height:160px}
.profile-area{padding:0 40px;position:relative}
.avatar{width:100px;height:100px;background:#1d2226;border-radius:50%;border:4px solid #1d2226;display:flex;align-items:center;justify-content:center;font-size:2.5em;margin-top:-50px;position:relative;z-index:1}
.name{font-size:1.5em;font-weight:bold;margin-top:15px;color:#ffffff}
.title{color:#b0b8c1;margin:6px 0}
.location{color:#b0b8c1;font-size:0.9em}
.contact-btn{background:#0a66c2;color:#fff;padding:8px 20px;border:none;cursor:pointer;margin:15px 0;font-family:'Courier New';font-size:0.9em}
.section{padding:20px 40px;border-top:1px solid #38434f;margin-top:10px}
.section h3{color:#ffffff;margin-bottom:12px}
.bio-text{color:#b0b8c1;line-height:1.7}
.bio-clue{color:#0a66c2;margin-top:10px}
a{color:#0a66c2;text-decoration:none}
a:hover{text-decoration:underline}
.skill-tag{background:#283e4a;color:#b0b8c1;padding:4px 12px;margin:4px;display:inline-block;border-radius:16px;font-size:0.85em}
</style></head>
<body>
<div class="header">in LinkedIn</div>
<div class="main">
  <div class="cover"></div>
  <div class="profile-area">
    <div class="avatar">&#128274;</div>
    <div class="name">Alex Turing</div>
    <div class="title">Senior Security Engineer at [CONFIDENCIAL] &middot; Ex-CorpCorp</div>
    <div class="location">&#128205; Lima, Per&uacute; &mdash; Open to opportunities</div>
    <button class="contact-btn">Connect</button>
  </div>
  <div class="section">
    <h3>Acerca de</h3>
    <div class="bio-text">
      <p>Ingeniero de seguridad con 8+ a&ntilde;os de experiencia en red team, threat hunting y arquitectura de seguridad.</p>
      <p style="margin-top:10px">Ex-CorpCorp (2019-2023). Denunci&eacute; irregularidades y ahora sigo la verdad donde sea que est&eacute;.</p>
      <p style="margin-top:10px">Mis proyectos personales est&aacute;n en mi GitLab: <strong><a href="/gitlab/a_turing">@a_turing</a></strong></p>
      <p class="bio-clue" style="margin-top:10px">&#128161; Fun fact: siempre uso ROT para cifrar mis memos personales. Old habit from my CTF days.</p>
    </div>
  </div>
  <div class="section">
    <h3>Habilidades</h3>
    <span class="skill-tag">Penetration Testing</span>
    <span class="skill-tag">Threat Hunting</span>
    <span class="skill-tag">OSINT</span>
    <span class="skill-tag">Python</span>
    <span class="skill-tag">Red Team</span>
    <span class="skill-tag">Cryptography</span>
    <span class="skill-tag">ROT Ciphers</span>
  </div>
  <div class="section">
    <h3>Experiencia</h3>
    <p><strong>CorpCorp S.A.</strong> &mdash; Security Engineer (2019 - 2023)</p>
    <p style="color:#b0b8c1;margin-top:4px;font-size:0.9em">Trabaj&eacute; en el equipo de seguridad interna. Acceso a infraestructura cr&iacute;tica.</p>
  </div>
</div>
</body></html>"""

GITLAB_PROFILE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>a_turing — GitLab</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1f1f1f;color:#e5e5e5;font-family:'Courier New',monospace;padding:0}
.header{background:#292961;padding:16px 40px;border-bottom:1px solid #3d3d8a;color:#fc6d26;font-size:1.1em}
.main{padding:40px;max-width:900px;margin:0 auto}
.avatar-area{display:flex;align-items:center;gap:20px;margin-bottom:30px}
.avatar{width:80px;height:80px;background:#2d2d2d;border-radius:50%;border:2px solid #fc6d26;display:flex;align-items:center;justify-content:center;font-size:2em}
.username{font-size:1.5em;color:#e5e5e5}
.bio{color:#a0a0a0;margin-top:6px}
.section{margin-top:30px}
.section h3{color:#fc6d26;margin-bottom:15px;border-bottom:1px solid #3d3d8a;padding-bottom:8px}
.repo{border:1px solid #3d3d8a;background:#2d2d2d;padding:16px;margin-bottom:12px;border-radius:4px}
.repo-name{color:#418cd8;font-size:1.1em;text-decoration:none}
.repo-name:hover{text-decoration:underline}
.repo-desc{color:#a0a0a0;margin-top:6px;font-size:0.9em}
.repo-meta{color:#6e6e6e;font-size:0.8em;margin-top:8px}
a{color:#418cd8;text-decoration:none}
a:hover{text-decoration:underline}
</style></head>
<body>
<div class="header">GitLab &mdash; a_turing</div>
<div class="main">
  <div class="avatar-area">
    <div class="avatar">&#129418;</div>
    <div>
      <div class="username">Alex Turing / @a_turing</div>
      <div class="bio">Security researcher. I encrypt everything. Always have.</div>
      <div style="color:#6e6e6e;margin-top:4px;font-size:0.85em">&#128205; Lima, Per&uacute; &nbsp; &#128274; Public repos only</div>
    </div>
  </div>

  <div class="section">
    <h3>Repositorios (2)</h3>
    <div class="repo">
      <a class="repo-name" href="/gitlab/a_turing/whistle-tools">whistle-tools</a>
      <div class="repo-desc">Tools I used during my time at CorpCorp. Anonymized.</div>
      <div class="repo-meta">Python &nbsp;|&nbsp; &Uacute;ltimo commit: hace 3 meses &nbsp;|&nbsp; &#11088; 127</div>
    </div>
    <div class="repo">
      <a class="repo-name" href="/gitlab/a_turing/personal-backup">personal-backup</a>
      <div class="repo-desc">Encrypted personal notes and backup configs. See README.</div>
      <div class="repo-meta">Shell &nbsp;|&nbsp; &Uacute;ltimo commit: hace 6 meses &nbsp;|&nbsp; &#11088; 3</div>
    </div>
  </div>
</div>
</body></html>"""

GITLAB_REPO = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>a_turing/personal-backup — GitLab</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1f1f1f;color:#e5e5e5;font-family:'Courier New',monospace;padding:0}
.header{background:#292961;padding:16px 40px;border-bottom:1px solid #3d3d8a;color:#fc6d26}
.main{padding:40px;max-width:900px;margin:0 auto}
.breadcrumb{color:#a0a0a0;margin-bottom:20px;font-size:0.9em}
.breadcrumb a{color:#418cd8;text-decoration:none}
.readme-box{border:1px solid #3d3d8a;background:#2d2d2d;padding:20px;border-radius:4px}
.readme-title{color:#fc6d26;margin-bottom:15px;font-size:1.1em}
.readme-content{color:#e5e5e5;line-height:1.8}
.code-block{background:#1a1a1a;border:1px solid #3d3d8a;padding:10px;margin:10px 0;font-family:monospace}
a{color:#418cd8;text-decoration:none}
a:hover{text-decoration:underline}
.file-list{border:1px solid #3d3d8a;border-radius:4px;margin-bottom:20px}
.file{padding:8px 16px;border-bottom:1px solid #3d3d8a;display:flex;gap:10px}
.file:last-child{border-bottom:none}
.file-icon{color:#fc6d26}
.file-name{color:#418cd8}
</style></head>
<body>
<div class="header">GitLab &mdash; a_turing / personal-backup</div>
<div class="main">
  <div class="breadcrumb"><a href="/gitlab/a_turing">a_turing</a> / personal-backup</div>

  <div class="file-list">
    <div class="file"><span class="file-icon">&#128196;</span><span class="file-name">README.md</span><span style="color:#6e6e6e;margin-left:auto">Update backup location &middot; 6 months ago</span></div>
    <div class="file"><span class="file-icon">&#128196;</span><span class="file-name">backup.sh</span><span style="color:#6e6e6e;margin-left:auto">Initial commit &middot; 6 months ago</span></div>
    <div class="file"><span class="file-icon">&#128196;</span><span class="file-name">.gitignore</span><span style="color:#6e6e6e;margin-left:auto">Initial commit &middot; 6 months ago</span></div>
  </div>

  <div class="readme-box">
    <div class="readme-title">&#128196; README.md</div>
    <div class="readme-content">
      <p><strong>Personal Backup System &mdash; Alex Turing</strong></p>
      <p style="margin-top:12px">This repo contains my backup scripts. Sensitive content is encrypted before storage.</p>
      <p style="margin-top:12px"><strong>Backup Location:</strong></p>
      <div class="code-block">Encrypted backup stored at: <a href="/paste/b4ckup_2024">/paste/b4ckup_2024</a></div>
      <p style="margin-top:12px"><strong>Encryption Method:</strong></p>
      <p>I use my personal encoding scheme. If you know me, you know how I encode everything.<br>
      Hint: check my LinkedIn bio for the method.</p>
      <p style="margin-top:12px;color:#6e6e6e;font-size:0.9em">Last backup: 2024-07-15</p>
    </div>
  </div>
</div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(NEWS_PAGE)

@app.route('/linkedin/alex-turing')
def linkedin():
    return render_template_string(LINKEDIN_PAGE)

@app.route('/gitlab/a_turing')
def gitlab_profile():
    return render_template_string(GITLAB_PROFILE)

@app.route('/gitlab/a_turing/personal-backup')
def gitlab_repo():
    return render_template_string(GITLAB_REPO)

@app.route('/gitlab/a_turing/whistle-tools')
def gitlab_tools():
    return render_template_string("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>a_turing/whistle-tools &mdash; GitLab</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#1f1f1f;color:#e5e5e5;font-family:'Courier New',monospace;padding:40px}.header{background:#292961;padding:16px;color:#fc6d26;margin-bottom:20px}.box{border:1px solid #3d3d8a;background:#2d2d2d;padding:20px}</style></head>
<body>
<div class="header">GitLab &mdash; a_turing / whistle-tools</div>
<div class="box">
  <p>Herramientas de auditor&iacute;a interna &mdash; anonimizadas. Sin contenido sensible en este repositorio.</p>
  <p style="margin-top:10px;color:#a0a0a0">Ver <a href="/gitlab/a_turing/personal-backup" style="color:#418cd8">personal-backup</a> para el backup cifrado.</p>
</div>
</body></html>""")

@app.route('/paste/b4ckup_2024')
def paste_backup():
    encoded = get_encoded_flag()
    PASTE = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>PasteCorp &mdash; b4ckup_2024</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}}
h1{{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}}
.box{{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}}
.meta{{color:#006600;font-size:0.85em;margin-bottom:15px}}
.content{{background:#001100;border:1px solid #003300;padding:15px;font-family:monospace;word-break:break-all;color:#00ff41;font-size:1.1em}}
.label{{color:#00cc33;margin-bottom:8px}}
.hint{{color:#009920;font-style:italic}}
</style></head>
<body>
<h1>[ PasteCorp &mdash; b4ckup_2024 ]</h1>
<div class="box">
  <div class="meta">Autor: a_turing &nbsp;|&nbsp; Creado: 2024-07-15 &nbsp;|&nbsp; <span style="color:#ffaa00">PRIVADO</span></div>
  <div class="label">Backup cifrado (m&eacute;todo personal):</div>
  <div class="content">{encoded}</div>
</div>
<div class="box">
  <p class="hint">El m&eacute;todo de cifrado est&aacute; en el perfil del autor &mdash; dos capas, el &uacute;ltimo primero.</p>
</div>
</body></html>"""
    return render_template_string(PASTE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
