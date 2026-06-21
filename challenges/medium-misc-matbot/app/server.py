#!/usr/bin/env python3
from flask import Flask, Response

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MathBot Corp — Verificacion Automatica</title>
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
    .port {{
      display: inline-block;
      background: #003300;
      color: #00ff41;
      padding: 0.15rem 0.6rem;
      font-size: 0.9rem;
      margin-right: 0.5rem;
    }}
    code {{
      background: #001a00;
      padding: 0.1rem 0.4rem;
      color: #00ff41;
    }}
    .stat-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
      margin-top: 0.75rem;
    }}
    .stat {{
      border: 1px solid #003300;
      padding: 0.75rem;
      text-align: center;
    }}
    .stat .val {{
      font-size: 1.4rem;
      color: #00ff41;
    }}
    .stat .lbl {{
      font-size: 0.75rem;
      color: #007700;
      margin-top: 0.2rem;
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
    <h1>[ MathBot Corp &mdash; Verificación Automática ]</h1>

    <div class="box">
      <h2>Descripcion</h2>
      <p>
        Un bot de verificación matemática espera conexiones en el puerto
        <span class="port">9999</span>.
        Responde 50 operaciones aritméticas en 30 segundos para demostrar
        que eres una máquina.
      </p>
    </div>

    <div class="box">
      <h2>Parametros del reto</h2>
      <div class="stat-grid">
        <div class="stat">
          <div class="val">50</div>
          <div class="lbl">operaciones</div>
        </div>
        <div class="stat">
          <div class="val">30s</div>
          <div class="lbl">tiempo límite</div>
        </div>
        <div class="stat">
          <div class="val">+&nbsp;-&nbsp;*</div>
          <div class="lbl">operadores</div>
        </div>
      </div>
    </div>

    <div class="box">
      <h2>Acceso</h2>
      <p>Conéctate con: <code>nc &lt;host&gt; 9999</code></p>
    </div>

    <p class="hint">El humano piensa, la máquina resuelve &mdash; escribe el script.</p>
  </div>
</body>
</html>"""


@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
