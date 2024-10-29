from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    """User model"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar = Column(String)
    sex = Column(String)
    name = Column(String)
    surname = Column(String)
    email = Column(String, nullable=False)

    def __str__(self):
        return f'Пользователь {self.email}.'
