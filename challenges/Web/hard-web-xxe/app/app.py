import os
from flask import Flask, request, render_template_string
from lxml import etree

app = Flask(__name__)
FLAG = os.environ.get('FLAG', 'HL4{placeholder_flag_here}')

# Write flag to file at startup (XXE reads the file, not env var)
with open('/flag.txt', 'w') as f:
    f.write(FLAG + '\n')

MAIN_PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>InvoicePro Corp</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}textarea{width:100%;height:160px;background:#001100;color:#00ff41;border:1px solid #003300;padding:10px;font-family:'Courier New',monospace;font-size:.85rem}button{background:#003300;color:#00ff41;border:1px solid #00ff41;padding:10px 24px;cursor:pointer;font-family:'Courier New',monospace}button:hover{background:#00ff41;color:#0a0a0a}.hint{color:#009920;font-style:italic}pre{background:#001100;padding:12px;font-size:.85rem;white-space:pre-wrap}</style></head><body>
<h1>InvoicePro Corp &mdash; XML Invoice Processor</h1>
<div class="box"><p>Sube tu factura en formato XML para procesamiento autom&aacute;tico.</p></div>
<div class="box"><h2 style="color:#00cc33;margin-bottom:10px">Enviar Factura XML</h2>
<form method="POST" action="/process">
<textarea name="xml_data">&lt;?xml version="1.0"?&gt;
&lt;invoice&gt;
  &lt;id&gt;INV-001&lt;/id&gt;
  &lt;amount&gt;1500.00&lt;/amount&gt;
  &lt;vendor&gt;CorpSupply Ltd&lt;/vendor&gt;
&lt;/invoice&gt;</textarea><br><br>
<button type="submit">Procesar Factura</button>
</form></div>
<div class="box"><p class="hint">El sistema conf&iacute;a en el XML que le env&iacute;as &mdash; quiz&aacute;s demasiado.</p></div>
</body></html>"""

RESULT_PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>InvoicePro Corp — Resultado</title>
<style>*{box-sizing:border-box;margin:0;padding:0}body{background:#0a0a0a;color:#00ff41;font-family:'Courier New',monospace;padding:40px}h1{color:#00ff41;border-bottom:1px solid #00ff41;padding-bottom:12px;margin-bottom:24px}.box{border:1px solid #003300;background:#050505;padding:20px;margin-bottom:20px}a{color:#00ff41}pre{background:#001100;padding:12px;font-size:.85rem;white-space:pre-wrap}</style></head><body>
<h1>Resultado del Procesamiento</h1>
<div class="box"><h2 style="color:#00cc33;margin-bottom:10px">Datos Procesados</h2>
<pre>{{result}}</pre></div>
<div class="box"><a href="/">&#8592; Volver</a></div>
</body></html>"""

@app.route('/')
def index():
    return render_template_string(MAIN_PAGE)

@app.route('/process', methods=['POST'])
def process():
    xml_data = request.form.get('xml_data', '')
    try:
        # VULNERABLE: resolve_entities=True allows XXE
        parser = etree.XMLParser(resolve_entities=True, no_network=False)
        root = etree.fromstring(xml_data.encode(), parser)
        # Extract and display all text content
        result_lines = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                result_lines.append(f"{elem.tag}: {elem.text.strip()}")
        result = '\n'.join(result_lines) if result_lines else "(vacío)"
    except Exception as e:
        result = f"Error procesando XML: {e}"
    return render_template_string(RESULT_PAGE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
