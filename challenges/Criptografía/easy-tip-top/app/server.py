from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Capas Invertidas</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 700px; margin: 0 auto; }
    h1 { color: #58a6ff; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #1f6feb; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .story { background: #161b22; border-left: 3px solid #58a6ff; border-radius: 0 6px 6px 0; padding: 18px 22px; margin-bottom: 28px; line-height: 1.9; color: #c9d1d9; font-style: italic; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
    li { margin-bottom: 6px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#128260; Capas Invertidas</h1>
    <span class="tag">easy &bull; criptografía</span>
    <div class="story">
      <p>El tiempo nunca avanzó en línea recta.</p>
      <p>Cada capa fue invertida antes de continuar.</p>
      <p>Solo quien siga el orden correcto podrá recuperar el mensaje original.</p>
    </div>
    <p class="desc">
      Alguien cifró un mensaje aplicando transformaciones en capas.
      Descarga el archivo, analiza el patrón y deshaz cada paso en el orden correcto.
    </p>
    <a href="/download" class="download-btn">&#11015; Descargar tip-top.txt</a>
    <div class="info">
      <h3>Pistas</h3>
      <ul style="padding-left:18px; line-height:2;">
        <li>Busca en tu corazón, y encontrarás la respuesta.</li>
      </ul>
    </div>
  </div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download')
def download():
    return send_file('/app/dist/tip-top.txt', as_attachment=True, download_name='tip-top.txt')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
