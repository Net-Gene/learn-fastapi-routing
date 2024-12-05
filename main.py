from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from controllers import categories, products, users
from custom_exceptions.not_found_exception import NotFoundexception
from custom_exceptions.unauthorized_exception import UnauthorizedException
from custom_exceptions.username_taken_exception import UsernameTakenException

app = FastAPI()


@app.exception_handler(NotFoundexception)
async def not_found_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=404)


@app.exception_handler(UsernameTakenException)
async def username_taken_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=400)


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=401)


@app.exception_handler(UnauthorizedException)
async def forbidden_exception_handler(request, exception):
    raise HTTPException(detail=str(exception), status_code=403)


app.include_router(users.router)

app.include_router(products.router)

app.include_router(categories.router)
