from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from controllers import products, users
from custom_exceptions.not_found_exception import NotFoundexception
from custom_exceptions.username_taken_exception import UsernameTakenException

app = FastAPI()


@app.exception_handler(NotFoundexception)
async def not_found(request: Request, exc: NotFoundexception):
    raise HTTPException(status_code=404, detail=str(exc))


@app.exception_handler(UsernameTakenException)
async def not_found(request: Request, exc: NotFoundexception):
    raise HTTPException(status_code=400, detail=str(exc))


app.include_router(users.router)

app.include_router(products.router)
