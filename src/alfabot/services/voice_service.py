import requests
import os
from faster_whisper import WhisperModel

# Carrega o modelo apenas uma vez para economizar memória
model = WhisperModel("base", device="cpu", compute_type="int8")

def baixar_audio(media_id, token):
    # 1. Obter a URL do arquivo
    url_media = f"https://graph.facebook.com/v20.0/{media_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url_media, headers=headers)
    url_download = response.json()['url']

    # 2. Baixar o arquivo .ogg
    audio_data = requests.get(url_download, headers=headers)
    caminho_local = f"data/temp_{media_id}.ogg"
    with open(caminho_local, "wb") as f:
        f.write(audio_data.content)
    return caminho_local

def transcrever_audio(caminho_arquivo):
    segments, info = model.transcribe(caminho_arquivo, language="pt")
    texto = "".join([segment.text for segment in segments])
    return texto.strip()