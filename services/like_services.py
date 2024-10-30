from models.likes import Like

from services.base_services import BaseService


class LikeService(BaseService):
    model = Like
