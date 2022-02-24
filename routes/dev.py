from datetime import timedelta
from fastapi import Depends, Response, Query, APIRouter, HTTPException
import uuid
import datetime
import db
import store
from config import config

DEV = config["dev"]


async def dev_only():
    if DEV == False:
        raise HTTPException(404)

router = APIRouter(dependencies=[Depends(dev_only)], prefix="/dev", tags=["development"])

# WIP


@router.get("/login")
def login_dev(response: Response, role: int = Query("2")):
    sid = uuid.uuid4()
    expires = datetime.now() + timedelta(days=7)
    store.set(f"sessions/{sid}", {"uid": "DEV", "expires": expires})
    response.set_cookie("enok_sid", sid, httponly=True, secure=False,
                        max_age=timedelta(days=7).total_seconds)
    return "sup"


@router.get("/users")
def read_root():
    users = db.get_table_data("users")
    return {"Hello": users}


@router.get("/store")
def read_store():
    return store.getAll()
