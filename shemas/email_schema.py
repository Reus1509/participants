from pydantic import BaseModel

class EmailSchema(BaseModel):
    to: str
    subject: str
    message: str