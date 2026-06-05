import flask
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Obtém o token de verificação que definimos no .env
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """Rota para a verificação inicial do Webhook da Meta"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Token inválido", 403

@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    """Rota para receber as mensagens do WhatsApp"""
    dados = request.json
    print(f"Mensagem recebida: {dados}")
    # Por enquanto, apenas confirmamos o recebimento
    return jsonify({"status": "recebido"}), 200

if __name__ == '__main__':
    app.run(port=5000)