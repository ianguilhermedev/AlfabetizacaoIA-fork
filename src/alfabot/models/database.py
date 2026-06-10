from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# --- CONFIGURAÇÃO DE CAMINHO ---
# Resolve o diretório raiz do projeto de forma robusta e cross-platform
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_DIR = PROJECT_ROOT / "data"

# Cria a pasta data automaticamente
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "alfabot.db"

# URL de conexão formatada para SQLite
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

    # Uso de datetime do Python com timezone para consistência absoluta
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime,
                        default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


def inicializar_banco():
    """Cria o arquivo do banco e as tabelas se não existirem."""
    Base.metadata.create_all(engine)