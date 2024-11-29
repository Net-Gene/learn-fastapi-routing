from fastapi import APIRouter, HTTPException

from dtos.users import UpdateUserDto, UserDto, AddUserReq, LoginReqDto, LoginResDto
from mapper.mapper import ResponseMapper
from services.service_factory import UserService
from tools.token_factory import AppToken

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


@router.post('/register')
def create_user(user_service: UserService, req: AddUserReq,
                mapper: ResponseMapper) -> UserDto:
    user = user_service.create(req)
    return mapper.map('user_dto', user)


@router.post('/login')
def login(user_service: UserService, req: LoginReqDto, _token: AppToken) -> LoginResDto:
    token_str = user_service.login(req, _token)
    return LoginResDto(token=token_str)
