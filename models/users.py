from sqlalchemy import Column, Integer, String, DateTime, DOUBLE
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
    registration_date = Column(DateTime)
    width = Column(DOUBLE)
    longitude = Column(DOUBLE)

    def __str__(self):
        return f'Пользователь {self.email}.'
