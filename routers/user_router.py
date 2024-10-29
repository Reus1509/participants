from typing import List

from fastapi import APIRouter, HTTPException,UploadFile, Response, Request
from database import sessionmaker
from PIL import Image

from shemas.users_shema import SUser
from services.user_services import UserService


router = APIRouter(
    prefix="/api",
    tags=["Участники"],
)

@router.post("/clients/create")
def create_user(user: SUser):
    existing_user = UserService.find_one_or_none(email = user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    UserService.add(avatar=user.avatar, sex=user.sex, name=user.name, surname=user.surname, email=user.email)


@router.post("/add_avatar")
async def add_user_avatar(request:Request, file: UploadFile):
    current_user_email = request.cookies.get("current_user")
    if not current_user_email:
        raise HTTPException(status_code=400, detail="Not logged in.")
    user = UserService.find_one_or_none(email=current_user_email)
    with sessionmaker() as session:
        user.avatar = file.filename
        session.add(user)
        session.commit()

    base_image = Image.open(file.file)
    watermark = Image.open("./static/watermark.png")

    base_image.paste(watermark, (0, 0), watermark)
    base_image.save(f"./static/{file.filename}.jpg")

@router.post("/delete_user/{user_id}")
def delete_user(user_id: int):
    UserService.delete(user_id)


@router.get("/all_users")
def get_all_users() -> List[SUser]:
    return UserService.find_all()


@router.post("/login/{user_email}")
def login_user(response: Response, user_email: str,):
    response.set_cookie("current_user", user_email, httponly=True)

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("current_user")

@router.get("/me")
def get_me(request: Request):
    current_user_email = request.cookies.get("current_user")
    user = UserService.find_one_or_none(email=current_user_email)
    return user
