#!/usr/bin/env python3
from flask import Flask, Response, send_from_directory
import os

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CorpCorp — Repositorio Interno</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0a0a0a;
      color: #00ff41;
      font-family: 'Courier New', Courier, monospace;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}
    .container {{
      max-width: 820px;
      width: 100%;
    }}
    h1 {{
      font-size: 1.6rem;
      letter-spacing: 0.1em;
      border-bottom: 1px solid #003300;
      padding-bottom: 0.75rem;
      margin-bottom: 1.5rem;
      color: #00ff41;
    }}
    .box {{
      border: 1px solid #003300;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.25rem;
      background: #050505;
    }}
    .box h2 {{
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: #009920;
      margin-bottom: 0.75rem;
    }}
    p {{
      font-size: 0.95rem;
      line-height: 1.7;
      color: #00cc35;
    }}
    a {{
      color: #00ff41;
      text-decoration: underline;
    }}
    a:hover {{
      color: #80ffb0;
    }}
    .download-btn {{
      display: inline-block;
      margin-top: 1rem;
      padding: 0.5rem 1.2rem;
      border: 1px solid #00ff41;
      color: #00ff41;
      text-decoration: none;
      font-family: 'Courier New', Courier, monospace;
      font-size: 0.9rem;
      letter-spacing: 0.05em;
      transition: background 0.2s;
    }}
    .download-btn:hover {{
      background: #003300;
      color: #00ff41;
    }}
    code {{
      background: #001a00;
      padding: 0.1rem 0.4rem;
      color: #00ff41;
    }}
    .hint {{
      margin-top: 2rem;
      text-align: center;
      font-size: 0.8rem;
      color: #005500;
      font-style: italic;
      letter-spacing: 0.05em;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>[ CorpCorp &mdash; Repositorio Interno ]</h1>

    <div class="box">
      <h2>Incidente de seguridad</h2>
      <p>
        Se filtró el repositorio interno de CorpCorp. El equipo de seguridad
        eliminó las credenciales sensibles del código fuente... ¿o eso creen?
      </p>
    </div>

    <div class="box">
      <h2>Descarga</h2>
      <p>El bundle del repositorio está disponible para análisis forense:</p>
      <a class="download-btn" href="/files/corp-repo.bundle">
        [descargar] corp-repo.bundle
      </a>
    </div>

    <div class="box">
      <h2>Instrucciones basicas</h2>
      <p>
        Clona el bundle con: <code>git clone corp-repo.bundle corp-repo</code><br>
        Luego investiga el historial de commits.
      </p>
    </div>

    <p class="hint">Lo que el git borra del árbol, el grafo de commits nunca olvida.</p>
  </div>
</body>
</html>"""


@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


@app.route("/files/<path:filename>")
def download(filename):
    return send_from_directory("/app/dist", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
