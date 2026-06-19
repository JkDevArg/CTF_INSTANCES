import os
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

def get_halves():
    mid = len(FLAG) // 2
    half1 = base64.b64encode(FLAG[:mid].encode()).decode()
    half2 = base64.b64encode(FLAG[mid:].encode()).decode()
    return half1, half2

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>DomainRecon — OSINT Tool</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
code{background:#001100;padding:2px 8px;color:#00ff41}
.endpoint{padding:8px;border-left:2px solid #003300;margin:8px 0}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.hint{color:#009920;font-style:italic}
</style></head>
<body>
<h1>[ DomainRecon — Herramienta de Reconocimiento de Dominio ]</h1>
<div class="box">
  <p>Investiga el dominio <strong>corpcorp.local</strong> utilizando las herramientas disponibles.</p>
  <p style="margin-top:10px">Se sabe que este dominio tiene registros WHOIS y entradas en logs de Certificate Transparency.</p>
</div>
<div class="box">
  <h2>Herramientas disponibles</h2>
  <div class="endpoint"><code>GET /whois?domain=corpcorp.local</code> — Consulta WHOIS</div>
  <div class="endpoint"><code>GET /ct-log?domain=corpcorp.local</code> — Certificate Transparency Log</div>
</div>
<div class="box">
  <p class="hint">Un dominio tiene dos historias — quién lo registró, y qué certificados emitió.</p>
</div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(INDEX)

@app.route('/whois')
def whois():
    domain = request.args.get('domain', '')
    half1, half2 = get_halves()

    if domain == 'corpcorp.local':
        WHOIS_RESP = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>WHOIS — {domain}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}}
h1{{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}}
.box{{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}}
.field{{padding:4px 0;display:flex;gap:20px}}
.key{{color:#009920;min-width:220px}}
.value{{color:#00ff41}}
.section{{color:#00cc33;margin:15px 0 8px;font-size:1.1em}}
</style></head>
<body>
<h1>[ WHOIS — {domain} ]</h1>
<div class="box">
  <div class="section">Domain Information</div>
  <div class="field"><span class="key">Domain Name:</span><span class="value">CORPCORP.LOCAL</span></div>
  <div class="field"><span class="key">Registry Domain ID:</span><span class="value">D-2024-CC-001</span></div>
  <div class="field"><span class="key">Created Date:</span><span class="value">2019-03-14T00:00:00Z</span></div>
  <div class="field"><span class="key">Updated Date:</span><span class="value">2024-01-01T00:00:00Z</span></div>
  <div class="field"><span class="key">Expiry Date:</span><span class="value">2027-03-14T00:00:00Z</span></div>
  <div class="field"><span class="key">Registrar:</span><span class="value">CorpRegistrar S.A.</span></div>
  <div class="field"><span class="key">Name Server:</span><span class="value">ns1.corpcorp.local</span></div>
  <div class="field"><span class="key">DNSSEC:</span><span class="value">unsigned</span></div>

  <div class="section">Registrant Contact</div>
  <div class="field"><span class="key">Organization:</span><span class="value">CorpCorp S.A.</span></div>
  <div class="field"><span class="key">Country:</span><span class="value">PE</span></div>
  <div class="field"><span class="key">State:</span><span class="value">Lima</span></div>
  <div class="field"><span class="key">Registrant Email:</span><span class="value">{half1}@corpcorp.local</span></div>
  <div class="field"><span class="key">Phone:</span><span class="value">+51.1.2345678</span></div>
  <div class="field"><span class="key">Admin Email:</span><span class="value">admin@corpcorp.local</span></div>

  <div class="section">Status</div>
  <div class="field"><span class="key">Domain Status:</span><span class="value">clientTransferProhibited</span></div>
</div>
</body></html>"""
        return WHOIS_RESP
    else:
        return render_template_string("""<!DOCTYPE html><html><head><meta charset="utf-8"><title>WHOIS — No encontrado</title><style>body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}.box{border:1px solid #003300;background:#050505;padding:20px}</style></head><body><div class="box"><p>Dominio no encontrado en la base de datos WHOIS.</p></div></body></html>""")

@app.route('/ct-log')
def ct_log():
    domain = request.args.get('domain', '')
    half1, half2 = get_halves()

    if domain == 'corpcorp.local':
        CT_RESP = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CT Log — {domain}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}}
h1{{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}}
.box{{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}}
.cert{{border:1px solid #002200;padding:15px;margin-bottom:15px}}
.field{{padding:3px 0;display:flex;gap:20px}}
.key{{color:#009920;min-width:200px}}
.value{{color:#00ff41;word-break:break-all}}
.section{{color:#00cc33;margin:12px 0 6px}}
.badge{{background:#003300;color:#00cc33;padding:2px 8px;font-size:0.8em}}
</style></head>
<body>
<h1>[ Certificate Transparency Log — {domain} ]</h1>
<div class="box">
  <p>Certificados registrados en CT Logs para el dominio <strong>{domain}</strong></p>
</div>

<div class="box">
  <div class="cert">
    <div class="section">Certificado #1 <span class="badge">VÁLIDO</span></div>
    <div class="field"><span class="key">Issuer:</span><span class="value">CorpCA Root 2024</span></div>
    <div class="field"><span class="key">Subject CN:</span><span class="value">corpcorp.local</span></div>
    <div class="field"><span class="key">Not Before:</span><span class="value">2024-01-01T00:00:00Z</span></div>
    <div class="field"><span class="key">Not After:</span><span class="value">2025-01-01T00:00:00Z</span></div>
    <div class="field"><span class="key">Serial:</span><span class="value">0x00A1B2C3D4E5F6</span></div>
    <div class="field"><span class="key">Subject Alt Names:</span><span class="value">corpcorp.local, www.corpcorp.local, api.corpcorp.local</span></div>
    <div class="field"><span class="key">CT Log ID:</span><span class="value">ct-corp-log-2024-01</span></div>
  </div>

  <div class="cert">
    <div class="section">Certificado #2 <span class="badge">EXPIRADO</span></div>
    <div class="field"><span class="key">Issuer:</span><span class="value">CorpCA Root 2023</span></div>
    <div class="field"><span class="key">Subject CN:</span><span class="value">internal.corpcorp.local</span></div>
    <div class="field"><span class="key">Not Before:</span><span class="value">2023-01-01T00:00:00Z</span></div>
    <div class="field"><span class="key">Not After:</span><span class="value">2024-01-01T00:00:00Z</span></div>
    <div class="field"><span class="key">Serial:</span><span class="value">0x00F1E2D3C4B5A6</span></div>
    <div class="field"><span class="key">Subject Alt Names:</span><span class="value">internal.corpcorp.local, {half2}.internal.corpcorp.local</span></div>
    <div class="field"><span class="key">CT Log ID:</span><span class="value">ct-corp-log-2023-99</span></div>
  </div>
</div>
</body></html>"""
        return CT_RESP
    else:
        return render_template_string("""<!DOCTYPE html><html><head><meta charset="utf-8"><title>CT Log — Sin resultados</title><style>body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}.box{border:1px solid #003300;background:#050505;padding:20px}</style></head><body><div class="box"><p>No se encontraron certificados para este dominio.</p></div></body></html>""")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
