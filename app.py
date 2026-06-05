import flask
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.alfabot.models.database import SessionLocal, LearnerProfile
from src.alfabot.services.whatsapp_service import enviar_mensagem_texto

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
    dados = request.json
    
    # Navegação segura pela estrutura do JSON da Meta
    entry = dados.get('entry', [])
    if entry:
        changes = entry[0].get('changes', [])
        if changes:
            value = changes[0].get('value', {})
            
            # Verificamos se 'messages' existe (pode ser notificação de leitura/entrega)
            messages = value.get('messages')
            
            if messages:
                mensagem_info = messages[0]
                numero = mensagem_info.get('from')
                
                # Verificamos se é realmente texto
                if mensagem_info.get('type') == 'text':
                    texto = mensagem_info.get('text', {}).get('body', '')
                    
                    # Lógica de Banco de Dados
                    session = SessionLocal()
                    try:
                        # Busca o aluno ou cria um novo
                        aluno = session.query(LearnerProfile).filter_by(phone_number=numero).first()
                        
                        if not aluno:
                            aluno = LearnerProfile(phone_number=numero, pedagogical_level='iniciante')
                            session.add(aluno)
                            session.commit()
                            print(f"Novo aluno registrado: {numero}")
                        
                        nivel_atual = aluno.pedagogical_level
                        
                        # Resposta personalizada baseada no nível do aluno
                        resposta = f"Olá! Seu nível atual é: {nivel_atual}. Você escreveu: {texto}"
                        enviar_mensagem_texto(numero, resposta)
                        
                    except Exception as e:
                        session.rollback()
                        print(f"Erro ao processar mensagem no banco: {e}")
                    finally:
                        session.close()

    return jsonify({"status": "recebido"}), 200

if __name__ == '__main__':
    app.run(port=5000)