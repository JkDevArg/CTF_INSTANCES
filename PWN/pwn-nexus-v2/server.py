from flask import Flask, send_file, render_template_string

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>NEXUS Terminal v2 — PWN</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 40px 20px; }
    .container { max-width: 760px; margin: 0 auto; }
    .header { border: 1px solid #00ff41; padding: 20px; margin-bottom: 30px; }
    .header pre { font-size: 0.82rem; line-height: 1.5; }
    h2 { color: #00ff41; font-size: 1.1rem; margin-bottom: 14px; border-bottom: 1px solid #1a3a1a; padding-bottom: 6px; }
    .section { margin-bottom: 28px; }
    .prot-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .prot-table td { padding: 5px 10px; border: 1px solid #1a3a1a; }
    .on  { color: #ff4444; }
    .off { color: #00ff41; }
    .btn { display: inline-block; background: #0a2a0a; border: 1px solid #00ff41; color: #00ff41;
           text-decoration: none; padding: 10px 22px; border-radius: 3px; font-family: inherit;
           font-size: 0.9rem; margin-right: 10px; margin-top: 6px; }
    .btn:hover { background: #1a4a1a; }
    .cmd { background: #0a1a0a; border: 1px solid #1a3a1a; padding: 10px 14px;
           border-radius: 3px; font-size: 0.85rem; color: #aaffaa; margin-top: 8px; }
    .hint { color: #558855; font-size: 0.82rem; margin-top: 10px; line-height: 1.6; }
    code { color: #aaffaa; }
    .flow { background: #0a1a0a; border-left: 3px solid #00ff41; padding: 12px 16px; margin-top: 8px;
            font-size: 0.82rem; line-height: 2; }
  </style>
</head>
<body>
<div class="container">
  <div class="header">
    <pre>================================================
  NEXUS Corp -- Secure Authentication Terminal
          >> Version 2.1 PATCHED <<
  [!] Stack canary & PIE protections active
================================================</pre>
  </div>

  <div class="section">
    <h2>Binary Protections</h2>
    <table class="prot-table">
      <tr><td>NX (No-Execute)</td>    <td class="on">ENABLED</td></tr>
      <tr><td>PIE</td>                <td class="on">ENABLED</td></tr>
      <tr><td>Stack Canary</td>       <td class="on">ENABLED</td></tr>
      <tr><td>RELRO</td>              <td>PARTIAL</td></tr>
      <tr><td>Architecture</td>       <td>x86-64 ELF, Ubuntu 22.04</td></tr>
    </table>
  </div>

  <div class="section">
    <h2>Downloads</h2>
    <a class="btn" href="/download/binary">nexus (ELF binary)</a>
    <a class="btn" href="/download/libc">libc.so.6 (glibc 2.35)</a>
    <p class="hint">
      Download both. Use <code>pwninit</code> or <code>patchelf</code> to link the binary
      against the provided libc for accurate local debugging.
    </p>
  </div>

  <div class="section">
    <h2>Connect</h2>
    <div class="cmd">nc &lt;host&gt; &lt;port&gt;  &nbsp;&nbsp;# address shown in CTFd when you launch the instance</div>
  </div>

  <div class="section">
    <h2>Exploit Flow</h2>
    <div class="flow">
      <strong>Step 1 — Format string (employee_lookup)</strong><br>
      &nbsp;&nbsp;Send <code>%p.%p.%p...</code> to dump the stack<br>
      &nbsp;&nbsp;Find: stack canary (8 bytes, lowest byte = 0x00) + libc return address<br><br>
      <strong>Step 2 — Stack overflow (authenticate)</strong><br>
      &nbsp;&nbsp;Frame: <code>[password 48B][canary 8B][saved_rbp 8B][rip 8B]</code><br>
      &nbsp;&nbsp;Payload: <code>A*48 + canary + A*8 + pop_rdi + /bin/sh + ret + system</code><br><br>
      <strong>Step 3 — Shell</strong><br>
      &nbsp;&nbsp;<code>cat flag.txt</code>
    </div>
    <p class="hint">
      &bull; Both bugs are in separate functions called sequentially from main()<br>
      &bull; You do not need to know the binary base — use only libc gadgets<br>
      &bull; Recommended: pwntools, pwndbg, <code>fmtstr_payload()</code>
    </p>
  </div>
</div>
</body>
</html>"""


@app.route('/')
def index():
    return render_template_string(PAGE)


@app.route('/download/binary')
def download_binary():
    return send_file('/home/ctf/download/nexus', as_attachment=True, download_name='nexus')


@app.route('/download/libc')
def download_libc():
    return send_file('/home/ctf/download/libc.so.6', as_attachment=True, download_name='libc.so.6')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
