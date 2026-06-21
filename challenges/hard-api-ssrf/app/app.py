import os
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, render_template_string

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WebhookProxy API</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d1117;
    color: #c9d1d9;
    font-family: 'Courier New', monospace;
    min-height: 100vh;
    padding: 40px 20px;
  }
  .container { max-width: 860px; margin: 0 auto; }
  h1 {
    font-size: 2.2rem;
    color: #ff6b6b;
    margin-bottom: 8px;
    letter-spacing: 2px;
  }
  .tag {
    display: inline-block;
    background: #6e040f;
    color: #ff9999;
    padding: 3px 12px;
    border-radius: 4px;
    font-size: 0.78rem;
    letter-spacing: 1px;
    margin-bottom: 28px;
    text-transform: uppercase;
  }
  .story {
    border-left: 3px solid #ff6b6b;
    padding: 14px 20px;
    font-style: italic;
    color: #8b949e;
    background: #161b22;
    border-radius: 0 6px 6px 0;
    margin-bottom: 32px;
  }
  h2 {
    color: #e6edf3;
    font-size: 1.1rem;
    margin-bottom: 14px;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px;
  }
  .endpoint {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 16px;
  }
  .method {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
    margin-right: 10px;
  }
  .get  { background: #1f6feb; color: #fff; }
  .post { background: #238636; color: #fff; }
  .ep-path { color: #79c0ff; font-size: 1rem; }
  .ep-desc { color: #8b949e; font-size: 0.88rem; margin-top: 8px; }
  pre {
    background: #010409;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    font-size: 0.85rem;
    color: #e6edf3;
    margin-top: 10px;
    line-height: 1.5;
  }
  .hint {
    margin-top: 36px;
    padding: 14px 20px;
    border: 1px dashed #6e040f;
    border-radius: 6px;
    color: #ff9999;
    font-size: 0.88rem;
    background: #0d0608;
  }
  .hint-label {
    color: #ff6b6b;
    font-weight: bold;
    display: block;
    margin-bottom: 4px;
  }
  .badge {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.8rem;
    color: #8b949e;
  }
</style>
</head>
<body>
<div class="container">
  <h1>WebhookProxy API</h1>
  <span class="tag">hard &bull; api</span>

  <div class="story">
    Un servicio de pruebas de webhooks permite verificar si tu endpoint responde
    correctamente. Envía una URL, el servidor la consulta y te devuelve la
    respuesta completa. Útil para depurar integraciones externas.
    El servidor tiene una red interna. Tu cliente, no.
  </div>

  <h2>Endpoints</h2>

  <div class="endpoint">
    <span class="method get">GET</span>
    <span class="ep-path">/api/status</span>
    <div class="ep-desc">Estado del servicio y versión actual.</div>
    <pre>curl -s http://&lt;host&gt;/api/status</pre>
  </div>

  <div class="endpoint">
    <span class="method post">POST</span>
    <span class="ep-path">/api/webhook/test</span>
    <div class="ep-desc">
      Prueba un webhook enviando una solicitud HTTP a la URL especificada.
      Devuelve el status HTTP y el cuerpo de la respuesta.<br><br>
      Body: <span class="badge">application/json</span>
      &nbsp;<code>{"url": "https://tu-servidor.com/hook"}</code>
    </div>
    <pre>curl -s -X POST http://&lt;host&gt;/api/webhook/test \\
  -H "Content-Type: application/json" \\
  -d '{"url": "https://httpbin.org/get"}'

# Respuesta:
{
  "status": 200,
  "body": "..."
}</pre>
  </div>

  <h2>Restricciones conocidas</h2>
  <pre># URLs bloqueadas explicitamente:
- 169.254.169.254  (AWS metadata)
- metadata.google  (GCP metadata)
- metadata.internal</pre>

  <div class="hint">
    <span class="hint-label">// HINT</span>
    El servidor puede consultar URLs externas. Pero el servidor
    tambien tiene una direccion. Y esa direccion tiene endpoints
    que no aparecen en esta pagina.
  </div>
</div>
</body>
</html>"""

app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/internal/config')
def internal_config():
    # Only accessible from localhost
    client_ip = request.remote_addr
    if client_ip not in ('127.0.0.1', '::1'):
        return jsonify({'error': 'Access restricted to internal network'}), 403
    return jsonify({
        'environment': 'production',
        'version': '2.1.4',
        'secret_key': FLAG,
        'db_host': 'postgres.internal',
        'debug': False,
    })


@app.route('/api/webhook/test', methods=['POST'])
def webhook_test():
    data = request.get_json(silent=True) or {}
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'url is required'}), 400
    if not url.startswith(('http://', 'https://')):
        return jsonify({'error': 'Invalid URL scheme'}), 400
    # Blocklist check (bypassable — 127.0.0.1, localhost, [::1] all work)
    blocked = ['169.254.169.254', 'metadata.google', 'metadata.internal']
    if any(b in url for b in blocked):
        return jsonify({'error': 'Blocked URL'}), 403
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'WebhookTester/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read(4096).decode('utf-8', errors='replace')
            return jsonify({'status': resp.status, 'body': body})
    except urllib.error.URLError as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 400
    except Exception:
        return jsonify({'error': 'Internal error'}), 500


@app.route('/api/status')
def status():
    return jsonify({'status': 'ok', 'service': 'WebhookProxy', 'version': '2.1.4'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
