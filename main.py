from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from controllers import categories, products, users, orders, carts
from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.general_exception import GeneralException
from custom_exceptions.missing_field_exception import MissingFieldException
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from custom_exceptions.username_taken_exception import UsernameTakenException

app = FastAPI()


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=404)


@app.exception_handler(UsernameTakenException)
async def username_taken_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=400)


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=401)


@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=403)


@app.exception_handler(MissingFieldException)
async def missing_field_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=404)


@app.exception_handler(GeneralException)
async def general_exception_handler(request, exception):
    raise GeneralException()


@app.middleware('http')
async def log_urls(request: Request, call_next):
    print("logging", request.url)
    return await call_next(request)


app.include_router(users.router)

app.include_router(products.router)

app.include_router(categories.router)

app.include_router(orders.router)

app.include_router(carts.router)
