from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///participants.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

sessionmaker = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
