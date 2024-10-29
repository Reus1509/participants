from models.users import User
import shutil

from services.base_services import BaseService

class UserService(BaseService):
    model = User
