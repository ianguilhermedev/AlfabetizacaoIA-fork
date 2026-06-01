import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN') or os.getenv('WHATSAPP_TOKEN')
PHONE_ID = os.getenv('PHONE_ID') or os.getenv('WHATSAPP_PHONE_ID')


def normalizar_numero(numero: str) -> str:
    return re.sub(r'\D', '', numero)

def enviar_mensagem(numero: str, texto: str) -> bool:
    if not TOKEN or not PHONE_ID:
        print('Erro: TOKEN e PHONE_ID precisam estar definidos no arquivo .env.')
        return False

    numero_limpo = normalizar_numero(numero)

    url = f'https://graph.facebook.com/v19.0/{PHONE_ID}/messages'

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }

    payload = {
        'messaging_product': 'whatsapp',
        'to': numero_limpo,
        'type': 'text',
        'text': {'body': texto},
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)

        if r.status_code == 200:
            print("Mensagem enviada com sucesso!")
            return True
        else:
            print(f"Erro {r.status_code}: {r.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return False


if __name__ == "__main__":
    meu_numero = "+55 91993572789"
    enviar_mensagem(meu_numero, "Olá! Este é um teste do Alfabot Marajoara.")