from fastapi import APIRouter
from typing import List
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from models import User, UserCreateSerializer,UserSerializer

user_router = APIRouter(prefix='/api/v1/user')


class Status(BaseModel):
    message: str
    
    
@user_router.get('/', response_model=List[UserSerializer])
async def get_users():
    return await UserSerializer.from_queryset(User.all())

@user_router.post('/', response_model=UserSerializer)
async def create_user(user:UserCreateSerializer):
    user_obj = await User.create(**user.model_dump(exclude_unset=True))
    return await UserSerializer.from_tortoise_orm(user_obj)

@user_router.get('/{id}/', response_model= UserSerializer)
async def get_user(id: int):
    return await UserSerializer.from_queryset_single(User.get(id=id))

@user_router.put('/{id}/', response_model=UserSerializer)
async def update_user(id:int, user:UserCreateSerializer):
    await User.filter(id=id).update(**user.model_dump(exclude_unset=True))
    return await UserSerializer.from_queryset_single(User.get(id=id))

@user_router.delete('/{id}/', response_model=Status)
async def delete_user(id: int):
    print('called')
    account = await User.filter(id=id).delete()
    if not account:
        raise HTTPException(status_code=404, detail=f'User {id} not found')
    return Status(message=f'Deleted User {id}')
