from dns.e164 import query
from mako.testing.helpers import result_lines
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.sync import update

from database import sessionmaker

class BaseService:
    model = None

    @classmethod
    def find_all(cls):
        with sessionmaker() as session:
            query = select(cls.model)
            result = session.execute(query)
            result = result.scalars().all()
            return result

    @classmethod
    def find_by_id(cls, model_id: int):
        with sessionmaker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = session.execute(query)
            result = result.scalar_one_or_none()
            return result

    @classmethod
    def find_one_or_none(cls, **kwargs):
        with sessionmaker() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = session.execute(query)
            result = result.scalar_one_or_none()
            return result

    @classmethod
    def add(cls, **kwargs):
        with sessionmaker() as session:
            query = insert(cls.model).values(**kwargs)
            session.execute(query)
            session.commit()

    @classmethod
    def delete(cls, user_id):
        with sessionmaker() as session:
            query = delete(cls.model).where(cls.model.id == user_id)
            session.execute(query)
            session.commit()
