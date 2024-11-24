from fastapi import APIRouter, HTTPException

import models
from dtos.users import UpdateUserDto, UserDto
from services.service_factory import UserService

router = APIRouter(prefix="/api/users", tags=['users'])


@router.get('/')
async def get_users(service: UserService):
    user_dtos = []
    users = service.get_all()

    for user in users:
        user_dto = UserDto(id=user.Id, username=user.UserName, role=user.Role)
        user_dtos.append(user_dto)

    return user_dtos


@router.get('/get_user_by_id')
async def get_user(user_id: int, service: UserService):
    user = service.get_by_id(user_id)

    if user is None:
        raise HTTPException(detail="User not found", status_code=404)

    return UserDto(id=user.Id, username=user.UserName, role=user.Role)


@router.put('/{user_id}')
async def update_user(user_id: int, service: UserService, req_data: UpdateUserDto) -> UserDto:
    user = service.update_user(user_id, req_data)
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    return UserDto(id=user.Id, username=user.UserName, role=user.Role)
