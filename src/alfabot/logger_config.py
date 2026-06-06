import sys
from loguru import logger
import os

# Garante que a pasta de logs existe na raiz do projeto
if not os.path.exists("logs"):
    os.makedirs("logs")

# Remove qualquer configuração padrão para evitar duplicidade
logger.remove()

# Configuração 1: Log no Console (para você ver enquanto desenvolve)
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>", level="INFO")

# Configuração 2: Log em Arquivo (para manter histórico de 10 dias)
logger.add("logs/alfabot.log", rotation="500 MB", retention="10 days", level="INFO")