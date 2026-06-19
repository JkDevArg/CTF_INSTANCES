import os
import io
import base64
from flask import Flask, render_template_string, send_file

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'CTF{placeholder_flag_here}')

INDEX = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CorpMail — Investigación de Email</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin:20px 0 10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.hint{color:#009920;font-style:italic}
.warn{color:#ffaa00}
ul{padding-left:20px;line-height:2}
</style></head>
<body>
<h1>[ CorpMail — Investigación de Email Corporativo ]</h1>
<div class="box">
  <p class="warn">[!] Email interceptado del servidor corporativo de CorpCorp S.A.</p>
  <p style="margin-top:10px">Un email marcado como CONFIDENCIAL fue extraído durante la auditoría.<br>
  Analiza <strong>todos sus encabezados</strong> para encontrar la información oculta.</p>
</div>
<div class="box">
  <h2>Archivo interceptado</h2>
  <ul>
    <li><a href="/email">confidential_q4.eml &mdash; Email Q4 Financial Results (CEO to Board)</a></li>
  </ul>
</div>
<div class="box">
  <p class="hint">Los headers de un email cuentan la historia que el cuerpo prefiere callar.</p>
</div>
</body></html>"""

def make_eml():
    flag_b64 = base64.b64encode(FLAG.encode()).decode()
    eml_content = f"""From: ceo@corpcorp.local
To: board@corpcorp.local
Subject: Q4 Financial Results - CONFIDENTIAL
Date: Mon, 15 Jan 2024 09:42:17 +0000
MIME-Version: 1.0
Message-ID: <q4-results-2024-01-15@corpcorp.local>
X-Mailer: CorpMail Enterprise v4.2
X-Priority: 1 (Highest)
X-Correlation-ID: {flag_b64}
X-Classification: CONFIDENTIAL
X-Retention-Policy: 7years
Content-Type: multipart/mixed; boundary="CORPMAIL_BOUNDARY_2024"

--CORPMAIL_BOUNDARY_2024
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 7bit

Estimado Directorio,

Adjunto encontrarán los resultados financieros preliminares del Q4 2023.
Todas las cifras están sujetas a auditoría final.

Puntos clave:
- Ingresos totales: $48.2M (↑ 12% vs Q4 2022)
- EBITDA: $8.7M (margen 18%)
- Nuevos clientes: 127 enterprise

Este documento es CONFIDENCIAL y solo para distribución interna.

Atentamente,
Oficina del CEO
CorpCorp S.A.

--CORPMAIL_BOUNDARY_2024
Content-Type: application/pdf; name="Q4_Results_2023.pdf"
Content-Disposition: attachment; filename="Q4_Results_2023.pdf"
Content-Transfer-Encoding: base64

JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmoKPDwvTGVuZ3RoIDMgMCBSL0ZpbHRlci9GbGF0
ZURlY29kZT4+CnN0cmVhbQp4nCvkMlAwUDC1NFIwMFAwtTRSMDIzMTQyMTI3NDc4MzcxNTEy
NTQ3ODM3MTUxMjU0NzgzNzE1MTI1NDc4MzcxNTEyCg==

--CORPMAIL_BOUNDARY_2024--
"""
    return eml_content

@app.route('/')
def index():
    return render_template_string(INDEX)

@app.route('/email')
def email():
    content = make_eml()
    buf = io.BytesIO(content.encode('utf-8'))
    return send_file(
        buf,
        mimetype='message/rfc822',
        download_name='confidential_q4.eml',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
