from fastapi import Depends


from fastapi import APIRouter, Depends

import db

from dependencies import logged_in

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_current_user(user: db.User = Depends(logged_in)):
    return user