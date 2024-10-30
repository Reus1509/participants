from email.mime.text import MIMEText
from lib2to3.fixes.fix_input import context
from smtplib import SMTP_SSL

from fastapi import HTTPException
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema
from dns.e164 import query
from mako.testing.helpers import result_lines
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.sync import update
from starlette.responses import HTMLResponse

from config import OWN_EMAIL, OWN_EMAIL_PASSWORD
from shemas.email_schema import EmailSchema
import config

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
    def find_all_with_params(cls, **kwargs):
        with sessionmaker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = session.execute(query)
            return result.mappings().all()

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

    @classmethod
    def send_mail(cls, email, user_name, user_email):

        template = """
        <html>
        <body>
        <p>
        Вы понравились {{ user_name }}! Почта участника: {{  user_email }}
        </p>
        </body>
        </html>
        """

        try:
            body = f'Вы понравились {user_name}! Почта участника: {user_email}'
            msg = MIMEText(body, 'plain')
            msg['Subject'] = 'Вы понравились!'
            msg['From'] = f'{config.OWN_EMAIL}'
            msg['To'] = email

            port = 465

            server = SMTP_SSL('smtp.gmail.com', port)
            server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)

            server.send_message(msg)
            server.quit()
            return JSONResponse({"message": "Mail sent successfully"}, status_code=200)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
