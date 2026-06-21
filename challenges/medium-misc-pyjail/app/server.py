#!/usr/bin/env python3
from flask import Flask, Response

app = Flask(__name__)

ALLOWED_BUILTINS = [
    'abs', 'bin', 'bool', 'bytes', 'chr', 'dict', 'dir',
    'getattr', 'hasattr', 'hex', 'id', 'int', 'isinstance',
    'len', 'list', 'oct', 'ord', 'print', 'range', 'repr',
    'str', 'tuple', 'type', 'vars'
]

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PyJail Corp — Sandbox v1.0</title>
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
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 0.5rem;
    }}
    td {{
      padding: 0.3rem 0.5rem;
      font-size: 0.88rem;
      color: #00cc35;
      border-bottom: 1px solid #001a00;
    }}
    td:first-child {{
      color: #00ff41;
      font-weight: bold;
      width: 30%;
    }}
    .hint {{
      margin-top: 2rem;
      text-align: center;
      font-size: 0.8rem;
      color: #005500;
      font-style: italic;
      letter-spacing: 0.05em;
    }}
    code {{
      background: #001a00;
      padding: 0.1rem 0.4rem;
      color: #00ff41;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>[ PyJail Corp &mdash; Sandbox v1.0 ]</h1>

    <div class="box">
      <h2>Descripcion</h2>
      <p>
        Un intérprete Python con builtins restringidos está corriendo en el puerto
        <span class="port">9999</span>. La flag vive en
        <code>/home/ctf/flag.txt</code> &mdash; si logras leerla.
      </p>
    </div>

    <div class="box">
      <h2>Acceso</h2>
      <p>
        Conéctate con: <code>nc &lt;host&gt; 9999</code>
      </p>
    </div>

    <div class="box">
      <h2>Builtins disponibles</h2>
      <table>
        {rows}
      </table>
    </div>

    <p class="hint">El árbol de clases nunca olvida sus raíces &mdash; y sus raíces tienen llaves.</p>
  </div>
</body>
</html>"""


def make_rows():
    rows = []
    for i, name in enumerate(ALLOWED_BUILTINS):
        rows.append(f"<tr><td>{name}</td><td>builtin</td></tr>")
    return "\n        ".join(rows)


@app.route("/")
def index():
    return Response(HTML.format(rows=make_rows()), mimetype="text/html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
