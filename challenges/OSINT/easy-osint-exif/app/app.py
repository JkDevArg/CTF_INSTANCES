import os, io
from flask import Flask, send_file, render_template_string
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

def make_image():
    img = Image.new('RGB', (800, 400), color=(15, 15, 25))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 780, 380], outline=(0, 100, 0), width=3)
    draw.text((50, 150), "HACKL4BS SUMMIT 2024", fill=(0, 200, 60))
    draw.text((50, 200), "Foto oficial del evento", fill=(0, 120, 40))
    draw.text((50, 250), "Uso interno — clasificado", fill=(0, 80, 20))
    info = PngInfo()
    info.add_text("Comment", FLAG)
    info.add_text("Author", "HACKL4BS Media Team")
    info.add_text("Copyright", "2024 HACKL4BS Corp")
    buf = io.BytesIO()
    img.save(buf, format='PNG', pnginfo=info)
    buf.seek(0)
    return buf

PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>MediaCorp — Archivo de Imágenes</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
h2{color:#00cc33;margin-bottom:10px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41;text-decoration:none}
a:hover{text-decoration:underline}
.hint{color:#009920;font-style:italic;margin-top:10px}
ul{padding-left:20px;line-height:2}
</style></head>
<body>
<h1>[ MediaCorp — Archivo de Imágenes ]</h1>
<div class="box">
  <p>Se encontró una imagen en el servidor de medios de HACKL4BS Corp.<br>
  Parece ser la foto oficial de un evento interno.<br>
  Analiza <strong>todos</strong> sus metadatos.</p>
</div>
<div class="box">
  <h2>Archivo disponible</h2>
  <ul>
    <li><a href="/foto">summit_2024.png &mdash; Foto oficial HACKL4BS Summit 2024</a></li>
  </ul>
</div>
<div class="box">
  <p class="hint">Las imágenes guardan más que píxeles — los metadatos también tienen memoria.</p>
</div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(PAGE)

@app.route('/foto')
def foto():
    buf = make_image()
    return send_file(buf, mimetype='image/png', download_name='summit_2024.png', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
