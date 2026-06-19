from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MiniVM</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 720px; margin: 0 auto; }
    h1 { color: #f0883e; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #9e4a1a; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
    .opcode-table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 0.82rem; }
    .opcode-table th { color: #58a6ff; text-align: left; padding: 4px 8px; border-bottom: 1px solid #30363d; }
    .opcode-table td { padding: 4px 8px; color: #8b949e; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#129302; MiniVM</h1>
    <span class="tag">medium &bull; reversing</span>
    <p class="desc">
      Someone built a tiny virtual machine in C and encoded their flag verification as bytecode.
      The VM has 3 opcodes. The bytecode is a static array inside the binary.
      Reverse the instruction set, trace the bytecode, extract the flag.
    </p>
    <a href="/download" class="download-btn">&#11015; Download Binary (x86-64 ELF)</a>
    <div class="info">
      <h3>VM Architecture</h3>
      <table class="opcode-table">
        <tr><th>Opcode</th><th>Args</th><th>Description</th></tr>
        <tr><td><code>0x01</code></td><td>index, expected</td><td>Check a transformed input byte against expected value</td></tr>
        <tr><td><code>0x02</code></td><td>—</td><td>Halt: success</td></tr>
        <tr><td><code>0x03</code></td><td>—</td><td>Halt: failure</td></tr>
      </table>
      <h3 style="margin-top:14px;">Tips</h3>
      <ul style="padding-left:18px; line-height:2;">
        <li>Find the bytecode array in the binary (<code>static const unsigned char</code>)</li>
        <li>Understand the transform applied to each input character</li>
        <li>Write a script to invert the transform over the bytecode</li>
        <li>Run it: <code>./vm_challenge &lt;flag&gt;</code></li>
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
    return send_file('/app/dist/vm_challenge', as_attachment=True, download_name='vm_challenge')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
