from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, Response, Request

from PIL import Image
from sqlalchemy import select

from shemas.users_shema import SUser
from services.user_services import UserService
from services.like_services import LikeService
from database import sessionmaker
from models.users import User

router = APIRouter(
    prefix="/api",
    tags=["Участники"],
)


@router.post("/clients/create")
def create_user(user: SUser):
    existing_user = UserService.find_one_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    UserService.add(avatar=user.avatar, sex=user.sex, name=user.name, surname=user.surname, email=user.email,
                    registration_date=user.registration_date, width=user.width, longitude=user.longitude)


@router.post("/add_avatar")
async def add_user_avatar(request: Request, file: UploadFile):
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


@router.get("/list")
def get_all_users(
        sex: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        sorted: bool | None = None,
):
    with sessionmaker() as session:
        if sex is not None:
            query = select(User).filter_by(sex=sex)
        if name is not None:
            query = select(User).filter_by(name=name)
        if surname is not None:
            query = select(User).filter_by(surname=surname)
        result = session.execute(query)
        if sorted is not None and sorted is True:
            return result.order_by(User.registration_date).scalars().all()
        return result.scalars().all()


@router.get("/list/sorting_by_distance")
def get_all_users_by_distance(
        request: Request,
        sorted: bool | None = None,
        distance: float | None = None,
):
    current_user_email = request.cookies.get("current_user")
    if not current_user_email:
        raise HTTPException(status_code=400, detail="Not logged in.")
    user = UserService.find_one_or_none(email=current_user_email)
    for i in range(1, 100):
        if i == None:
            break
        if i == user.id:
            continue
        user_2 = UserService.find_one_or_none(id=i)
        with sessionmaker() as session:
            distance_user_2 = UserService.great_cicle_distnce(user.width, user.longitude, user_2.width,
                                                              user_2.longitude)
            user_2.distance = distance_user_2
            session.add(user_2)
            session.commit()
            if distance_user_2 < distance:
                return user_2


@router.post("/login/{user_email}")
def login_user(response: Response, user_email: str, ):
    user = UserService.find_one_or_none(email=user_email)
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")
    response.set_cookie("current_user", user_email, httponly=True)


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("current_user")


@router.get("/me")
def get_me(request: Request):
    current_user_email = request.cookies.get("current_user")
    user = UserService.find_one_or_none(email=current_user_email)
    return user


@router.post("/clients/{id}/match")
def add_like(id: int, request: Request):
    current_user_email = request.cookies.get("current_user")
    if not current_user_email:
        raise HTTPException(status_code=400, detail="Not logged in.")
    user = UserService.find_one_or_none(email=current_user_email)
    like_from = user.id
    like_to = id
    like_date = datetime.now()
    user_from = UserService.find_one_or_none(id=id)
    user_from_email = user_from.email
    LikeService.add(like_from=like_from, like_to=like_to, like_date=like_date)
    result = LikeService.find_one_or_none(like_from=like_to, like_to=like_from)
    if result != None:
        UserService.send_mail(user_from_email, user.name, user.email)


@router.post("/delete_like/{like_id}")
def delete_like(like_id: int):
    LikeService.delete(like_id)
