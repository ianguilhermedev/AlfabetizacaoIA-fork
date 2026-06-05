import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker

# --- CONFIGURAÇÃO DE CAMINHO ---
# O ideal é que o banco não fique no OneDrive.
# Se o erro persistir, altere 'DB_DIR' abaixo para uma pasta fora do OneDrive,
# como 'C:/alfabot_data/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR)) # Sobe para a raiz do projeto
DB_DIR = os.path.join(PROJECT_ROOT, 'data')

os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'alfabot.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()

# Adicionado check_same_thread=False para compatibilidade com Flask/Threads
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class LearnerProfile(Base):
    __tablename__ = 'learner_profiles'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    pedagogical_level = Column(String, default='iniciante')
    onboarding_state = Column(String, default='new')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

def inicializar_banco():
    """Cria o arquivo do banco e as tabelas se não existirem."""
    Base.metadata.create_all(engine)