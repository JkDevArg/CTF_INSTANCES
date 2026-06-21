import os
import secrets
from flask import Flask, request, jsonify, render_template_string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}').encode()
# Key is fixed for the lifetime of this container instance
KEY = secrets.token_bytes(16)


def oracle(user_input: bytes) -> bytes:
    """Encrypts user_input + FLAG under AES-ECB with a fixed key."""
    plaintext = pad(user_input + FLAG, 16)
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(plaintext)


PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>La Caja Negra</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 720px; margin: 0 auto; }
    h1 { color: #ff7b72; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #6e040f; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .story { background: #161b22; border-left: 3px solid #ff7b72; border-radius: 0 6px 6px 0; padding: 18px 22px; margin-bottom: 28px; line-height: 1.9; color: #c9d1d9; font-style: italic; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 24px; }
    .api-box { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 20px; margin-bottom: 24px; }
    .api-box h3 { color: #58a6ff; font-size: 0.95rem; margin-bottom: 14px; }
    .api-box pre { background: #0d1117; padding: 12px; border-radius: 4px; font-size: 0.82rem; color: #79c0ff; overflow-x: auto; line-height: 1.6; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 24px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
    li { margin-bottom: 6px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#11035; La Caja Negra</h1>
    <span class="tag">hard &bull; criptografía</span>
    <div class="story">
      <p>El servicio acepta cualquier texto y devuelve su versión cifrada.</p>
      <p>Nadie sabe qué hay dentro. Nadie puede verlo directamente.</p>
      <p>Pero la caja siempre añade algo al final antes de cifrar.</p>
    </div>
    <p class="desc">
      El servicio expone un oráculo de cifrado: puedes enviar cualquier dato
      y recibirás el resultado cifrado. La clave es fija. El secreto también.
      Extráelo byte a byte.
    </p>
    <div class="api-box">
      <h3>API — Oráculo de cifrado</h3>
      <pre>POST /encrypt
Content-Type: application/json

{ "data": "&lt;hex string&gt;" }

→ { "ciphertext": "&lt;hex string&gt;" }</pre>
    </div>
    <div class="info">
      <h3>Pista</h3>
      <ul style="padding-left:18px; line-height:2;">
        <li>Los bloques idénticos producen salidas idénticas. Siempre.</li>
      </ul>
    </div>
  </div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        body = request.get_json(silent=True) or {}
        hex_data = body.get('data', '')
        if not isinstance(hex_data, str) or len(hex_data) > 512:
            return jsonify({'error': 'invalid input'}), 400
        user_input = bytes.fromhex(hex_data)
    except (ValueError, TypeError):
        return jsonify({'error': 'invalid hex'}), 400

    ciphertext = oracle(user_input)
    return jsonify({'ciphertext': ciphertext.hex()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
