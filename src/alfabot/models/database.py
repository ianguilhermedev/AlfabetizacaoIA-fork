from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Define a localização do banco SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'alfabot.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class LearnerProfile(Base):
    __tablename__ = 'learner_profiles'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    # Níveis: 'iniciante', 'basico', 'intermediario'
    pedagogical_level = Column(String, default='iniciante')
    # Estados: 'new', 'collecting_level', 'active'
    onboarding_state = Column(String, default='new')
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

def inicializar_banco():
    """Cria o arquivo do banco e as tabelas se não existirem."""
    # Garante que a pasta 'data' existe
    os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
    Base.metadata.create_all(engine)