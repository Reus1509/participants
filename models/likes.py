from sqlalchemy import Column, Integer, DateTime
from database import Base


class Like(Base):
    """Likes model"""
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    like_from = Column(Integer, nullable=False)
    like_to = Column(Integer, nullable=False)
    like_date = Column(DateTime, nullable=False)

    def __str__(self):
        return f"Лайк от {self.like_from} для {self.like_to} от {self.like_date}."