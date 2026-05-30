#!/usr/bin/env python3
"""
Lab02 Flask interno — solo accesible desde la red internal.
Representa un servicio interno que no debería ser público.
"""
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/internal/flag")
def flag():
    return jsonify({
        "flag": "FLAG{ssrf_1nt3rn4l_s3rv1c3_3xp0s3d}",
        "hint": "Flag #3 — SSRF a servicio interno",
        "secret": "Este endpoint no debería ser accesible desde internet"
    })

@app.route("/internal/config")
def config():
    return jsonify({
        "db_host": "redis:6379",
        "db_pass": "REDACTED",
        "env": "production",
        "hint": "Intenta acceder a redis directamente via SSRF"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
