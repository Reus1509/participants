from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr
from typing import Optional


class SUser(BaseModel):
    id: int
    avatar: Optional[str] = None
    sex: Literal["male", "female"] = None
    name: str
    surname: str
    email: EmailStr
    registration_date: datetime
    width: Optional[float] = None
    longitude: Optional[float] = None
    distance: Optional[int] = None
