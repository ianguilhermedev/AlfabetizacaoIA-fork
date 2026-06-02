from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def create_engine_for_url(database_url: str):
    engine_kwargs = {"future": True}
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        if database_url in {"sqlite://", "sqlite:///:memory:"}:
            engine_kwargs["poolclass"] = StaticPool
    return create_engine(database_url, **engine_kwargs)


def get_session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


def init_database(engine) -> None:
    Base.metadata.create_all(engine)
