from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Crackme 01</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 680px; margin: 0 auto; }
    h1 { color: #f0883e; font-size: 1.5rem; margin-bottom: 8px; }
    .tag { display: inline-block; background: #9e4a1a; color: white; font-size: 0.72rem; padding: 2px 8px; border-radius: 3px; margin-bottom: 20px; text-transform: uppercase; }
    .desc { color: #8b949e; line-height: 1.7; margin-bottom: 28px; }
    .download-btn { display: inline-block; background: #238636; color: white; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 1rem; }
    .download-btn:hover { background: #2ea043; }
    .info { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 18px; margin-top: 28px; font-size: 0.85rem; color: #8b949e; }
    .info code { color: #79c0ff; background: #0d1117; padding: 1px 5px; border-radius: 3px; }
    h3 { color: #c9d1d9; font-size: 0.95rem; margin-bottom: 10px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>&#128640; Crackme 01</h1>
    <span class="tag">medium &bull; reversing</span>
    <p class="desc">
      A stripped ELF binary with no symbols. It reads your input from stdin and validates it
      using a per-character mathematical transformation. No anti-debug tricks — just math.
      Reverse the transform, recover the flag.
    </p>
    <a href="/download" class="download-btn">&#11015; Download Binary (x86-64 ELF)</a>
    <div class="info">
      <h3>Hints</h3>
      <ul style="padding-left:18px; line-height:2;">
        <li>Run it: <code>./crackme</code> — enters interactive mode</li>
        <li>Binary is stripped: no function names in <code>nm</code></li>
        <li>The transform is applied per character using its index</li>
        <li>Think: modular arithmetic and inverses</li>
        <li>Recommended: <code>ghidra</code>, <code>radare2 -A</code></li>
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
    return send_file('/app/dist/crackme', as_attachment=True, download_name='crackme')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
