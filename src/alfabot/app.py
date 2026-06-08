import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.alfabot.logger_config import logger

# Importações do seu projeto
from src.alfabot.models.database import SessionLocal, LearnerProfile, inicializar_banco
from src.alfabot.services.whatsapp_service import enviar_mensagem_texto
from src.alfabot.services.ai_service import gerar_resposta_ia
from src.alfabot.services.voice_service import baixar_audio, transcrever_audio

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# --- INICIALIZAÇÃO DO BANCO ---
with app.app_context():
    inicializar_banco()
    logger.info("Banco de dados verificado e tabelas criadas com sucesso.")

# Obtém o token de verificação que definimos no .env
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    """Rota para a verificação inicial do Webhook da Meta"""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("Webhook verificado com sucesso pela Meta.")
        return challenge, 200
    else:
        logger.warning(f"Tentativa inválida de verificação de webhook. Token recebido: {token}")
        return "Token inválido", 403


@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    dados = request.json
    logger.debug(f"Payload recebido da Meta: {dados}")

    if not dados or 'entry' not in dados:
        return jsonify({"status": "recebido"}), 200

    for entry in dados.get('entry', []):
        for change in entry.get('changes', []):
            value = change.get('value', {})
            messages = value.get('messages')

            if not messages:
                continue

            for mensagem_info in messages:
                numero = mensagem_info.get('from')
                tipo_msg = mensagem_info.get('type')
                texto_para_processar = ""

                logger.info(f"Nova mensagem recebida de {numero} (Tipo: {tipo_msg})")

                # --- LÓGICA DE NORMALIZAÇÃO DE ENTRADA ---
                if tipo_msg == 'text':
                    texto_para_processar = mensagem_info.get('text', {}).get('body', '')
                    logger.debug(f"Texto recebido: '{texto_para_processar}'")

                elif tipo_msg == 'audio':
                    media_id = mensagem_info.get('audio', {}).get('id')
                    token = os.getenv("WHATSAPP_TOKEN")

                    logger.info(f"Processando áudio com Media ID: {media_id}")
                    try:
                        caminho_audio = baixar_audio(media_id, token)
                        texto_para_processar = transcrever_audio(caminho_audio)
                        logger.info(f"Áudio transcrito com sucesso: '{texto_para_processar}'")

                        if os.path.exists(caminho_audio):
                            os.remove(caminho_audio)
                            logger.debug(f"Arquivo temporário removido: {caminho_audio}")
                    except Exception as e:
                        logger.error(f"Falha ao processar arquivo de áudio de {numero}: {e}")

                # --- FLUXO ÚNICO DE PROCESSAMENTO (IA + BANCO) ---
                if texto_para_processar.strip():
                    session = SessionLocal()
                    try:
                        aluno = session.query(LearnerProfile).filter_by(phone_number=numero).first()
                        if not aluno:
                            aluno = LearnerProfile(phone_number=numero, pedagogical_level='iniciante')
                            session.add(aluno)
                            session.commit()
                            logger.info(f"Novo aluno registrado no banco: {numero}")

                        nivel_atual = aluno.pedagogical_level
                        logger.info(f"Buscando resposta da IA para {numero} (Nível: {nivel_atual})")

                        resposta_ia = gerar_resposta_ia(texto_para_processar, nivel_atual)
                        enviar_mensagem_texto(numero, resposta_ia)
                        logger.info(f"Resposta enviada com sucesso para {numero}")

                    except Exception as e:
                        session.rollback()
                        logger.error(f"Erro no processamento do fluxo principal para {numero}: {e}")
                    finally:
                        session.close()
                else:
                    if tipo_msg == 'audio':
                        logger.warning(f"O áudio enviado por {numero} não gerou transcrição.")
                        enviar_mensagem_texto(numero,
                                              "Não consegui entender o áudio. Pode gravar novamente, por favor?")

    return jsonify({"status": "recebido"}), 200


if __name__ == '__main__':
    logger.info("Iniciando o servidor Flask de desenvolvimento na porta 5000...")
    app.run(port=5000)