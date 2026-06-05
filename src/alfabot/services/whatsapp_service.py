import os
import requests
from dotenv import load_dotenv

# Garante que as variáveis de ambiente sejam lidas 
load_dotenv()

def enviar_mensagem_texto(phone_number: str, texto: str) -> bool:
    """
    Envia uma mensagem de texto simples via WhatsApp Cloud API.
    """
    # Coleta o Token e o Phone ID do arquivo .env
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("WHATSAPP_PHONE_ID")

    # Proteção rápida: avisa se faltar alguma configuração no .env
    if not token or not phone_id:
        print("Erro: WHATSAPP_TOKEN ou WHATSAPP_PHONE_ID não configurados no .env")
        return False

    # Monta a URL da API da Meta
    url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"

    # Configura o cabeçalho (headers) obrigatório
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Monta o corpo da mensagem (payload) no formato JSON exigido
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": texto}
    }

    try:
        # Fazer a requisição usando requests.post com timeout de segurança
        resposta = requests.post(url, headers=headers, json=payload, timeout=10)

        # Retorna True se o status for 200 (OK) ou 201 (Created)
        if resposta.status_code in [200, 201]:
            print(f"Mensagem enviada com sucesso para {phone_number}!")
            return True
        else:
            # Imprime o erro detalhado da Meta caso algo dê errado
            print(f"Erro ao enviar mensagem: {resposta.status_code} - {resposta.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API da Meta: {e}")
        return False