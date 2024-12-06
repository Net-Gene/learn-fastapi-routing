from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from custom_exceptions.taken_exception import TakenException
from dependencies import LoggedInUser, require_admin
from dtos.users import UpdateUserDto, UserDto, AddUserReq, LoginReqDto, LoginResDto
from mapper.mapper import ResponseMapper
from services.service_factory import UserService
from tools.token_factory import AppToken

router = APIRouter(prefix="/api/users", tags=['users'])


@router.get('/',
            # Vain admin voi käyttää tätä routea, jos tämä rivi on aktiivinen
            # dependencies=[Depends(require_admin)]
            # Vain kirjautunut voi käyttää tätä routea, jos tämä rivi on aktiivinen
            # dependencies=[Depends(oauth2_scheme)]
            )
async def get_users(service: UserService, mapper: ResponseMapper):
    # user_dtos = []
    users = service.get_all()

    return mapper.map('user_dto', users)


@router.get('/account')
async def get_account(account: LoggedInUser, mapper: ResponseMapper) -> UserDto:
    return mapper.map('user_dto', account)


@router.post('/register')
def create_user(user_service: UserService, req: AddUserReq,
                mapper: ResponseMapper) -> UserDto:
    user = user_service.create(req)
    return mapper.map('user_dto', user)


@router.post('/login')
def login(user_service: UserService, req: LoginReqDto, _token: AppToken) -> LoginResDto:
    token_str = user_service.login(req, _token)
    return LoginResDto(token=token_str)


@router.get('/{user_id}')
async def get_user(user_id: int, service: UserService, mapper: ResponseMapper):
    user = service.get_by_id(user_id)

    if user is None:
        raise TakenException()

    return mapper.map('user_dto', user)


@router.put('/{user_id}')
async def update_user(user_id: int, service: UserService, req_data: UpdateUserDto, mapper: ResponseMapper) -> UserDto:
    user = service.update_user(user_id, req_data)
    if user is None:
        raise TakenException()
    return mapper.map('user_dto', user)
