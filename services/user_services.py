from models.users import User
from services.base_services import BaseService


class UserService(BaseService):
    model = User
