from typing import Type, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models

router = APIRouter(
    prefix="/api/users",
    tags=['users']
)


@router.get('/')
async def get_users(context: models.Db):
    users = context.query(models.Users).all()
    return users

