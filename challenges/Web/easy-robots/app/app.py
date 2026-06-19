from flask import Flask, Response
import os

app = Flask(__name__)
FLAG = os.environ.get('FLAG') or 'HL4{placeholder_flag_here}'


@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AcmeCorp</title>
  <style>
    body { background: #0d1117; color: #c9d1d9; font-family: Arial, sans-serif; max-width: 800px; margin: 80px auto; padding: 0 20px; }
    h1 { color: #58a6ff; }
    nav a { color: #58a6ff; margin-right: 20px; text-decoration: none; }
    nav a:hover { text-decoration: underline; }
    footer { margin-top: 80px; color: #444; font-size: 0.8rem; }
  </style>
</head>
<body>
  <nav><a href="/">Home</a><a href="/about">About</a><a href="/contact">Contact</a></nav>
  <h1>Welcome to AcmeCorp</h1>
  <p>We build things. Fast. Secure. Reliable.</p>
  <p style="color:#555; margin-top:40px;">Nothing to see here. Move along.</p>
  <footer>AcmeCorp &copy; 2024 &mdash; All rights reserved</footer>
</body>
</html>''', 200


@app.route('/robots.txt')
def robots():
    return Response(
        'User-agent: *\n'
        'Disallow: /admin/\n'
        'Disallow: /backup/\n'
        'Disallow: /internal/s3cr3t-dump/\n',
        mimetype='text/plain'
    )


@app.route('/admin/')
def admin():
    return '<h1>403 Forbidden</h1><p>Access denied.</p>', 403


@app.route('/backup/')
def backup():
    return '<h1>403 Forbidden</h1><p>Access denied.</p>', 403


@app.route('/internal/s3cr3t-dump/')
def secret_dump():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Internal Dump</title>
  <style>
    body {{ background:#0d1117; color:#c9d1d9; font-family:monospace; max-width:600px; margin:80px auto; padding:0 20px; }}
    pre {{ background:#161b22; border:1px solid #30363d; padding:20px; border-radius:6px; }}
  </style>
</head>
<body>
  <h2>&#128196; Internal Data Dump</h2>
  <p>This endpoint should not be publicly accessible.</p>
  <pre>{FLAG}</pre>
</body>
</html>''', 200


@app.route('/about')
def about():
    return '<h1>About AcmeCorp</h1><p>We exist.</p>', 200


@app.route('/contact')
def contact():
    return '<h1>Contact</h1><p>No one is home.</p>', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
