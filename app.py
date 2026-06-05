import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
# Adicionado 'inicializar_banco' ao seu import:
from src.alfabot.models.database import SessionLocal, LearnerProfile, inicializar_banco
from src.alfabot.services.whatsapp_service import enviar_mensagem_texto
from src.alfabot.services.ai_service import gerar_resposta_ia
from src.alfabot.services.voice_service import baixar_audio, transcrever_audio

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# --- INICIALIZAÇÃO DO BANCO ---
# Isso garante que a tabela 'learner_profiles' seja criada automaticamente
# antes do servidor começar a responder requisições.
with app.app_context():
    inicializar_banco()
    print("Banco de dados verificado e tabelas criadas com sucesso.")

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
    entry = dados.get('entry', [])
    
    if not entry: return jsonify({"status": "recebido"}), 200
    
    value = entry[0].get('changes', [{}])[0].get('value', {})
    messages = value.get('messages')
    
    if messages:
        mensagem_info = messages[0]
        numero = mensagem_info.get('from')
        tipo_msg = mensagem_info.get('type')
        texto_para_processar = ""

        # --- LÓGICA DE NORMALIZAÇÃO DE ENTRADA ---
        if tipo_msg == 'text':
            texto_para_processar = mensagem_info.get('text', {}).get('body', '')

        elif tipo_msg == 'audio':
            media_id = mensagem_info.get('audio', {}).get('id')
            token = os.getenv("WHATSAPP_TOKEN")
            
            # Baixa, transcreve e limpa
            caminho_audio = baixar_audio(media_id, token)
            texto_para_processar = transcrever_audio(caminho_audio)
            
            # Remove o arquivo .ogg após transcrever para economizar espaço
            if os.path.exists(caminho_audio):
                os.remove(caminho_audio)

        # --- FLUXO ÚNICO DE PROCESSAMENTO (IA + BANCO) ---
        if texto_para_processar.strip():
            session = SessionLocal()
            try:
                aluno = session.query(LearnerProfile).filter_by(phone_number=numero).first()
                if not aluno:
                    aluno = LearnerProfile(phone_number=numero, pedagogical_level='iniciante')
                    session.add(aluno)
                    session.commit()
                
                nivel_atual = aluno.pedagogical_level
                resposta_ia = gerar_resposta_ia(texto_para_processar, nivel_atual)
                enviar_mensagem_texto(numero, resposta_ia)
            except Exception as e:
                session.rollback()
                print(f"Erro no processamento: {e}")
            finally:
                session.close()
        else:
            # Caso o áudio esteja em branco ou corrompido
            if tipo_msg == 'audio':
                enviar_mensagem_texto(numero, "Não consegui entender o áudio. Pode gravar novamente, por favor?")

    return jsonify({"status": "recebido"}), 200

if __name__ == '__main__':
    app.run(port=5000)