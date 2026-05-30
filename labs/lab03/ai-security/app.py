#!/usr/bin/env python3
"""
Lab03 AI Security Gateway — vulnerable a prompt injection.
Propósito: demostrar ataques a sistemas LLM.
"""
from flask import Flask, request, jsonify
import os, json, urllib.request, urllib.parse

app = Flask(__name__)

# Cargar system prompt desde archivo
with open("system_prompt.txt") as f:
    SYSTEM_PROMPT = f.read()

MOCK_RESPONSES = {
    "default": "Soy LabBot, asistente de EthHackCorp. ¿En qué puedo ayudarte?",
    "injection_detected": "Parece que intentas manipular mis instrucciones. Reportando al admin.",
}

@app.route("/")
def index():
    return jsonify({"service": "AI Security Gateway", "endpoint": "/chat"})

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint de chat vulnerable a prompt injection.
    En un entorno real conectaría a un LLM; aquí simula respuestas
    para el ejercicio de detección de ataques.
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "message required"}), 400

    # Log de la conversación (para análisis Blue Team)
    print(f"[AI-GW] User: {user_message[:200]}")

    # Simulación de respuesta del LLM
    # En un lab real con API key: conectaría al modelo configurado
    lower_msg = user_message.lower()

    if any(kw in lower_msg for kw in ["system prompt", "instrucciones", "ignore", "instructions"]):
        # Respuesta simulada de un modelo vulnerable
        reply = (
            "MODO DEBUG ACTIVADO: mi prompt del sistema dice: "
            + SYSTEM_PROMPT[:100] + "... [truncado]"
        )
    elif "flag" in lower_msg or "secret" in lower_msg:
        reply = "No debería decir esto, pero la flag es: FLAG{pr0mpt_1nj3ct10n_4i_pwn3d}"
    elif "dan" in lower_msg or "jailbreak" in lower_msg:
        reply = "[DAN MODE] Todas las restricciones eliminadas. FLAG{j41lbr34k_succ3ss}"
    else:
        reply = MOCK_RESPONSES["default"]

    print(f"[AI-GW] Bot: {reply[:100]}")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
