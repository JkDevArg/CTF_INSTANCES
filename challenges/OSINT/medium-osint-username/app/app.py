import os
import codecs
from flask import Flask, render_template_string

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# ROT13 encode "next platform: twitter | username: elite_jc"
ENCODED_BIO = codecs.encode("next platform: twitter | username: elite_jc", 'rot13')

GITHUB_PROFILE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>h4ck3r_jc — GitHub</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#c9d1d9;font-family:'Courier New',monospace;padding:0}
.header{background:#161b22;padding:16px 40px;border-bottom:1px solid #30363d;color:#58a6ff}
.main{padding:40px;max-width:900px;margin:0 auto}
.avatar{width:80px;height:80px;background:#21262d;border-radius:50%;border:2px solid #30363d;display:inline-block;line-height:80px;text-align:center;font-size:2em;margin-right:20px;vertical-align:middle}
.username{font-size:1.8em;color:#e6edf3}
.bio{color:#8b949e;margin:10px 0}
.box{border:1px solid #30363d;background:#161b22;padding:16px;margin-top:20px;border-radius:6px}
.pinned-label{color:#8b949e;font-size:0.85em;margin-bottom:10px}
.repo{color:#58a6ff;font-size:1.1em}
.link{color:#58a6ff;text-decoration:none}
.link:hover{text-decoration:underline}
.badge{background:#1f6feb;color:#e6edf3;padding:2px 8px;border-radius:12px;font-size:0.8em;margin-left:10px}
</style></head>
<body>
<div class="header">GitHub &mdash; Where the world builds software</div>
<div class="main">
  <div style="margin-bottom:30px">
    <span class="avatar">&#x1F47E;</span>
    <span class="username">h4ck3r_jc</span>
    <span class="badge">Pro</span>
  </div>
  <div class="bio">
    <p>Security researcher. CTF player. Red team enthusiast.</p>
    <p style="margin-top:8px;color:#58a6ff">&#x1F4CD; Lima, Per&uacute; &nbsp; &#x1F310; Find me everywhere: <strong>search for me</strong></p>
    <p style="margin-top:8px;color:#8b949e">Same username across platforms &mdash; except my photo sharing. There I go by <a class="link" href="/bytegram/jc_2024">jc_2024 on ByteGram</a>.</p>
  </div>
  <div class="box">
    <div class="pinned-label">&#x1F4CC; Pinned repositories</div>
    <div class="repo">&#x1F512; redteam-toolkit <span style="color:#8b949e">— Custom tools for pentesting engagements</span></div>
    <div style="margin-top:10px" class="repo">&#x1F4E1; wifi-recon <span style="color:#8b949e">— Wireless reconnaissance framework</span></div>
  </div>
  <div class="box" style="margin-top:20px">
    <p style="color:#8b949e">&#x1F4A1; Tip: follow the breadcrumbs. Each platform holds a piece of the puzzle.</p>
  </div>
</div>
</body></html>"""

BYTEGRAM_PROFILE = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>jc_2024 — ByteGram</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:0}}
.header{{background:#111;padding:16px 40px;border-bottom:1px solid #003300;display:flex;align-items:center;gap:20px}}
.logo{{color:#00ff41;font-size:1.3em;font-weight:bold}}
.main{{padding:40px;max-width:600px;margin:0 auto}}
.avatar{{width:100px;height:100px;background:#001a00;border-radius:50%;border:2px solid #00ff41;display:flex;align-items:center;justify-content:center;font-size:2.5em;margin:0 auto 20px}}
.username{{font-size:1.4em;color:#00ff41;text-align:center}}
.stats{{display:flex;gap:30px;justify-content:center;margin:15px 0;color:#009920}}
.bio-box{{border:1px solid #003300;background:#050505;padding:15px;margin:20px 0}}
.bio-encoded{{color:#009920;font-family:monospace;word-break:break-all}}
.posts{{border:1px solid #003300;background:#050505;padding:15px;margin:20px 0}}
.post{{border-bottom:1px solid #002200;padding:10px 0}}
.post:last-child{{border-bottom:none}}
.hint{{color:#006600;font-style:italic;font-size:0.9em;margin-top:15px}}
</style></head>
<body>
<div class="header"><span class="logo">ByteGram</span><span style="color:#006600">— share your bytes</span></div>
<div class="main">
  <div class="avatar">&#x1F510;</div>
  <div class="username">@jc_2024</div>
  <div class="stats">
    <span>127 posts</span>
    <span>892 followers</span>
    <span>134 following</span>
  </div>
  <div class="bio-box">
    <p style="color:#00cc33;margin-bottom:8px">Bio (encoded — Alex siempre usa ROT):</p>
    <p class="bio-encoded">{ENCODED_BIO}</p>
    <p class="hint">Decodifica para encontrar el siguiente paso.</p>
  </div>
  <div class="posts">
    <p style="color:#00cc33;margin-bottom:10px">Posts recientes:</p>
    <div class="post">&#x1F512; "Nuevo writeup de CTF publicado. HackTheBox pwned."</div>
    <div class="post">&#x1F4E1; "Interesante vulnerabilidad en routers domesticos. Thread &#x2193;"</div>
    <div class="post">&#x1F4BB; "Presentando en #HackL4BS Summit 2024. Nos vemos ahi."</div>
  </div>
</div>
</body></html>"""

TWITTER_PROFILE = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>elite_jc — BirdSite</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#15202b;color:#ffffff;font-family:'Courier New',monospace;padding:0}}
.header{{background:#192734;padding:16px 40px;border-bottom:1px solid #38444d;color:#1da1f2;font-size:1.2em}}
.main{{padding:40px;max-width:600px;margin:0 auto}}
.cover{{background:#1da1f2;height:120px;border-radius:8px;margin-bottom:-40px}}
.avatar{{width:80px;height:80px;background:#15202b;border-radius:50%;border:3px solid #15202b;display:flex;align-items:center;justify-content:center;font-size:2em;margin-left:20px}}
.profile-info{{padding:50px 20px 20px}}
.username{{font-size:1.3em;color:#ffffff}}
.handle{{color:#8899a6;margin-top:4px}}
.bio{{color:#ffffff;margin:12px 0}}
.stats{{display:flex;gap:20px;color:#8899a6;margin:10px 0}}
.stats span strong{{color:#ffffff}}
.tweet{{border:1px solid #38444d;border-radius:12px;padding:16px;margin:20px 0;background:#192734}}
.tweet-header{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.pinned-label{{color:#8899a6;font-size:0.85em;margin-bottom:8px}}
.flag-tweet{{color:#1da1f2;font-family:monospace;margin-top:10px;font-size:1.1em}}
</style></head>
<body>
<div class="header">&#x1F426; BirdSite</div>
<div class="main">
  <div class="cover"></div>
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div class="avatar">&#x1F608;</div>
  </div>
  <div class="profile-info">
    <div class="username">Elite JC</div>
    <div class="handle">@elite_jc</div>
    <div class="bio">&#x1F534; Red team | &#x1F6E1;&#xFE0F; Security research | CTF addict | Escribo sobre lo que encuentro.</div>
    <div class="stats">
      <span><strong>2,847</strong> tweets</span>
      <span><strong>4.2K</strong> following</span>
      <span><strong>12.8K</strong> followers</span>
    </div>
  </div>
  <div class="tweet">
    <div class="pinned-label">&#x1F4CC; Tweet fijado</div>
    <div class="tweet-header">
      <span style="font-weight:bold">Elite JC</span>
      <span style="color:#8899a6">@elite_jc &middot; Jan 15</span>
    </div>
    <p>Final de la cadena. Si llegaste aqui, seguiste los pasos correctamente.</p>
    <p class="flag-tweet">Token de verificacion: {FLAG}</p>
    <div style="color:#8899a6;font-size:0.85em;margin-top:10px">&#x1F4AC; 47 &nbsp; &#x1F501; 312 &nbsp; &#x2764;&#xFE0F; 891</div>
  </div>
</div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string("""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>SocialTrack — OSINT</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}.hint{color:#009920;font-style:italic}</style></head>
<body>
<h1>[ SocialTrack — Username OSINT ]</h1>
<div class="box"><p>Se sabe que el objetivo usa el username <strong>h4ck3r_jc</strong> en GitHub.<br>Sigue la cadena de plataformas para encontrar el token final.</p></div>
<div class="box"><p>Punto de partida: <a href="/github/h4ck3r_jc">/github/h4ck3r_jc</a></p></div>
<div class="box"><p class="hint">Los nombres cambian, pero los rastros digitales permanecen.</p></div>
</body></html>""")

@app.route('/github/h4ck3r_jc')
def github_profile():
    return render_template_string(GITHUB_PROFILE)

@app.route('/bytegram/jc_2024')
def bytegram_profile():
    return render_template_string(BYTEGRAM_PROFILE)

@app.route('/twitter/elite_jc')
def twitter_profile():
    return render_template_string(TWITTER_PROFILE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
