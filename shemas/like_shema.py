from datetime import datetime
from pydantic import BaseModel

class SLike(BaseModel):
    id: int
    like_from: int
    like_to: int
    like_date: datetime