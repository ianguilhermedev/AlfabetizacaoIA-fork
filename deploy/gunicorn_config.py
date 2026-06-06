import multiprocessing

# O número de workers é geralmente (2 x núcleos da CPU) + 1
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:5000"

# Logs (usando a pasta que configuramos no Loguru)
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"