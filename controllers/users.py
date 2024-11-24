from fastapi import APIRouter, HTTPException

from dtos.users import UpdateUserDto, UserDto
from mapper.mapper import ResponseMapper
from services.service_factory import UserService

router = APIRouter(prefix="/api/users", tags=['users'])


@router.get('/')
async def get_users(service: UserService, mapper: ResponseMapper):
    users = service.get_all()

    return mapper.map('user_dto', users)


@router.get('/get_user_by_id')
async def get_user(user_id: int, service: UserService, mapper: ResponseMapper):
    user = service.get_by_id(user_id)

    if user is None:
        raise HTTPException(detail="User not found", status_code=404)

    return mapper.map('user_dto', user)


@router.put('/{user_id}')
async def update_user(user_id: int, service: UserService, req_data: UpdateUserDto, mapper: ResponseMapper) -> UserDto:
    user = service.update_user(user_id, req_data)
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    return mapper.map('user_dto', user)
