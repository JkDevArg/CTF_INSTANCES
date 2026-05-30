#!/usr/bin/env python3
"""
Lab01 Flask Target — aplicación vulnerable educativa.
Solo para entornos de laboratorio aislados.
"""
from flask import Flask, request, jsonify, make_response
import hashlib, os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "insecure_fallback")

USERS = {
    "admin": {"hash": hashlib.md5(b"admin123").hexdigest(), "role": "admin"},
    "user1": {"hash": hashlib.md5(b"password").hexdigest(), "role": "user"},
    "guest": {"hash": hashlib.md5(b"guest").hexdigest(),    "role": "guest"},
}

@app.route("/")
def index():
    return jsonify({"lab": "Lab01", "endpoints": ["/login", "/admin", "/profile", "/health"]})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/login", methods=["POST"])
def login():
    """Vulnerable: sin rate limiting, hash MD5 débil."""
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    user = USERS.get(username)
    if user and user["hash"] == hashlib.md5(password.encode()).hexdigest():
        resp = make_response(jsonify({"status": "ok", "role": user["role"]}))
        resp.set_cookie("session_user", username)   # sin HttpOnly — propósito educativo
        return resp
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

@app.route("/admin")
def admin():
    if request.cookies.get("session_user") == "admin":
        return jsonify({"flag": "FLAG{br3ak_w34k_4uth_b4s1c}", "hint": "Flag #2 — Brute Force HTTP"})
    return jsonify({"status": "forbidden"}), 403

@app.route("/profile")
def profile():
    u = request.cookies.get("session_user")
    if u and u in USERS:
        return jsonify({"user": u, "role": USERS[u]["role"]})
    return jsonify({"status": "unauthenticated"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
