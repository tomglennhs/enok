from datetime import timedelta, datetime
from fastapi import Depends, Response, Query, APIRouter, HTTPException
import uuid
import db
import db.users
import store
from config import config


async def dev_only():
    if not config.dev:
        raise HTTPException(404)


router = APIRouter(dependencies=[Depends(dev_only)],
                   prefix="/dev", tags=["development"])


@router.get("/login")
def login_dev(response: Response, role: db.Role = Query(2)):
    now = datetime.now()
    user = db.users.create_user("Dev User", f"dev@{now.timestamp()}.local", "dev", None, role)
    sid = uuid.uuid4()
    delta = timedelta(**config.sessionTimeout.dict())
    expires = now + delta
    store.set(f"sessions/{sid}", {"uid": user.id, "expires": expires})
    response.set_cookie("enok_sid", str(sid), httponly=True, secure=False,
                        max_age=int(delta.total_seconds()))
    return user


@router.get("/users")
def read_root():
    users = db.get_table_data("users")
    return {"Hello": users}


@router.get("/store")
def read_store():
    return store.getAll()
