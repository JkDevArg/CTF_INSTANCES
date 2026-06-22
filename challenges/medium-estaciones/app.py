import os
from flask import Flask, render_template_string, send_from_directory, request, jsonify

app = Flask(__name__)

SECRET_ANSWER = "HL4{3r05_5p4_n0rt3}
"  # <-- reemplaza con la flag hardcodeada del reto

PAGE_FLAG = os.environ.get('FLAG', 'FLAG_NOT_CONFIGURED')

MAIN = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Fugitivo — Caso Abierto</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41}p{line-height:1.7}
.hint{color:#009920;font-style:italic}
.flag-form input[type=text]{
  width:100%;padding:10px 14px;background:#050505;border:1px solid #003300;
  border-radius:6px;color:#00ff41;font-family:'Courier New',monospace;
  font-size:0.95rem;margin-bottom:10px;
}
.flag-form button{
  background:#003300;color:#00ff41;border:1px solid #00ff41;padding:10px 24px;
  border-radius:6px;font-size:0.95rem;cursor:pointer;font-family:'Courier New',monospace;
}
.flag-form button:hover{background:#005500;}
#flag-result{margin-top:14px;padding:12px 16px;border-radius:6px;font-size:0.9rem;display:none;}
#flag-result.ok {background:#0d2b1a;border:1px solid #238636;color:#3fb950;}
#flag-result.err{background:#2b0d0d;border:1px solid #da3633;color:#f85149;}
</style></head><body>
<h1>Investigaci&oacute;n Abierta &mdash; El Fugitivo</h1>
<div class="box">
<p>Él escap&oacute; un d&iacute;a de diciembre, cuando la ciudad inaugur&oacute; nuevas estaciones en el norte.<br>
Se dice que, tras tomarse la foto, fue a descansar a alg&uacute;n lugar reconocible desde lejos.<br>
Nunca pasa por ning&uacute;n sitio sin dejar rastro.<br><br>
Encuentra el &uacute;ltimo rastro que dej&oacute;.</p>
</div>
<div class="box">
<h2 style="color:#00cc33;margin-bottom:10px">Evidencia fotogr&aacute;fica</h2>
<ul style="padding-left:20px">
<li><a href="/foto">fugitivo.png &mdash; Foto tomada en el lugar de la fuga</a></li>
</ul>
</div>
<div class="box">
<h2 style="color:#00cc33;margin-bottom:10px">Pistas</h2>
<ul style="padding-left:20px">
<li>La foto fue tomada en diciembre de 2023 en Lima, Per&uacute;</li>
<li>El letrero visible dice &quot;Embarque Norte 1&quot;</li>
<li>Hay una letra &quot;B&quot; en fondo celeste en la estructura</li>
<li>Desde ese punto se ve una &quot;H&quot; iluminada a la izquierda</li>
<li>El fugitivo fue a descansar cerca &mdash; revisa las rese&ntilde;as del lugar</li>
</ul>
</div>
<div class="box">
<h2 style="color:#00cc33;margin-bottom:10px">Recursos de investigaci&oacute;n</h2>
<ul style="padding-left:20px">
<li><a href="/maps/hotel-eros-spa">Rese&ntilde;as Hotel Eros Spa &mdash; Google Maps (local cache)</a></li>
<li><a href="/maps/metropolitano">Metropolitano Lima &mdash; Ampliaci&oacute;n Norte 2023</a></li>
</ul>
</div>
<div class="box flag-form">
<h2 style="color:#00cc33;margin-bottom:10px">&#128275; Ingresa la flag</h2>
<input type="text" id="answer-input" placeholder="HL4{...}" autocomplete="off" spellcheck="false" />
<button type="button" onclick="submitAnswer()">Verificar</button>
<div id="flag-result"></div>
</div>
<div class="box"><p class="hint">El rastro no siempre est&aacute; en la imagen &mdash; a veces est&aacute; en lo que el sujeto opina.</p></div>
</body>
<script>
  function submitAnswer() {
    var answer = document.getElementById('answer-input').value.trim();
    var result = document.getElementById('flag-result');
    result.style.display = 'none';
    if (!answer) return;
    fetch('/verify', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({answer: answer})
    })
    .then(function(r){ return r.json(); })
    .then(function(d){
      result.style.display = 'block';
      if (d.success) {
        result.className = 'ok';
        result.innerHTML = '&#9989; Flag: <code style="color:#3fb950">' + d.flag + '</code>';
      } else {
        result.className = 'err';
        result.textContent = '&#10060; ' + (d.message || 'Respuesta incorrecta');
      }
    })
    .catch(function(){ result.className='err'; result.style.display='block'; result.textContent='Error de conexión'; });
  }
  document.getElementById('answer-input').addEventListener('keydown', function(e){
    if (e.key === 'Enter') submitAnswer();
  });
</script>
</html>"""

MAPS_HOTEL = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Hotel Eros Spa — Reseñas</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#121212;color:#e8eaed;font-family:'Google Sans',Arial,sans-serif;padding:0}
.header{background:#1f1f1f;padding:16px 24px;border-bottom:1px solid #333}
.header h1{color:#8ab4f8;font-size:1.1rem;font-weight:500}
.header p{color:#9aa0a6;font-size:.85rem;margin-top:4px}
.stars{color:#fbbc04;font-size:1.1rem}
.reviews{max-width:700px;margin:24px auto;padding:0 16px}
.review{background:#1f1f1f;border-radius:8px;padding:16px;margin-bottom:16px;border:1px solid #333}
.reviewer{font-weight:600;color:#e8eaed;margin-bottom:4px}
.date{color:#9aa0a6;font-size:.8rem;margin-bottom:8px}
.text{color:#e8eaed;line-height:1.6;font-size:.9rem}
a{color:#8ab4f8;text-decoration:none}
.back{padding:16px 24px}
</style></head><body>
<div class="header">
<h1>Hotel Eros Spa &mdash; Rese&ntilde;as de usuarios</h1>
<p>Av. Túpac Amaru, Independencia, Lima &nbsp;|&nbsp; <span class="stars">★★★☆☆</span> 3.2 (147 rese&ntilde;as)</p>
</div>
<div class="back"><a href="/">← Volver a la investigaci&oacute;n</a></div>
<div class="reviews">
<div class="review">
<div class="reviewer">Marco R.</div>
<div class="date">hace 2 meses <span class="stars">★★★★☆</span></div>
<div class="text">Buena ubicaci&oacute;n, cerca del Metropolitano. Personal amable. El cuarto un poco pequeño pero limpio.</div>
</div>
<div class="review">
<div class="reviewer">Usuarios_An&oacute;nimo_47</div>
<div class="date">hace 3 meses <span class="stars">★★★☆☆</span></div>
<div class="text">Tranqui, limpio, buena ubicaci&oacute;n cerca del Metropolitano. Vine despu&eacute;s de una noche movida y dorm&iacute; como beb&eacute;. {{FLAG}}</div>
</div>
<div class="review">
<div class="reviewer">Luciana P.</div>
<div class="date">hace 4 meses <span class="stars">★★☆☆☆</span></div>
<div class="text">El agua caliente falla en las mañanas. No volver&iacute;a.</div>
</div>
<div class="review">
<div class="reviewer">Jos&eacute; M.</div>
<div class="date">hace 5 meses <span class="stars">★★★★★</span></div>
<div class="text">Excelente para una estancia r&aacute;pida. Precio justo. Lo recomiendo si llegas tarde del aeropuerto.</div>
</div>
<div class="review">
<div class="reviewer">Carla F.</div>
<div class="date">hace 6 meses <span class="stars">★★★☆☆</span></div>
<div class="text">Normal. Ni muy bueno ni muy malo. La cama es c&oacute;moda.</div>
</div>
</div>
</body></html>"""

MAPS_METRO = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Metropolitano Lima — Ampliación Norte</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}
h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}
.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}
a{color:#00ff41}p{line-height:1.7}
</style></head><body>
<h1>Metropolitano de Lima &mdash; Ampliaci&oacute;n Norte 2023</h1>
<div class="box">
<p><strong>15 de diciembre de 2023</strong> &mdash; Inauguraci&oacute;n de 4 nuevas estaciones:<br><br>
1. Estaci&oacute;n Universidad<br>
2. Estaci&oacute;n 22 de Agosto<br>
3. Estaci&oacute;n Andr&eacute;s Belaunde<br>
4. Estaci&oacute;n Los Incas<br><br>
Las estaciones del Embarque Norte 1 corresponden al sistema BRT de Lima.<br>
La señal&iacute;tica usa c&oacute;digos de color: <strong>B</strong> en fondo celeste = Ruta B (Barranco &rarr; Independencia).
</p>
</div>
<div class="box">
<p>La Estaci&oacute;n Andr&eacute;s Belaunde es la &uacute;nica desde la que se observa una "H" iluminada al oeste &mdash;<br>
correspondiente al letrero del <strong>Hotel Eros Spa</strong>, a 180 metros de la salida norte.</p>
</div>
<div class="box"><a href="/">← Volver</a></div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(MAIN)

@app.route('/foto')
def foto():
    return send_from_directory('/app/static', 'fugitivo.png', as_attachment=True)

@app.route('/maps/hotel-eros-spa')
def hotel():
    return MAPS_HOTEL.replace('{{FLAG}}', SECRET_ANSWER)

@app.route('/maps/metropolitano')
def metro():
    return render_template_string(MAPS_METRO)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json(silent=True) or {}
    answer = (data.get('answer') or '').strip()
    if answer == SECRET_ANSWER:
        return jsonify({'success': True, 'flag': PAGE_FLAG})
    return jsonify({'success': False, 'message': 'Respuesta incorrecta'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)