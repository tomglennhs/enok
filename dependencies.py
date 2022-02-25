from fastapi import HTTPException, Response, Cookie
from enum import Enum
import store
import datetime
import db


class Role(Enum):
    VIEW_ONLY = 0
    STANDARD = 1
    ADMIN = 2


# TODO: Figure out how this needs to work
def auth_level(response: Response, enok_sid: str = Cookie(None), level: Role = 0):
    print(enok_sid)
    if enok_sid == None:
        raise HTTPException(401, "Please sign in.")
    key = f"sessions/{enok_sid}"
    session = store.get(key)
    if session == None or session["expires"] < datetime.now():
        response.set_cookie("enok_sid", enok_sid, max_age=-1)
        store.safeDelete(key)
        raise HTTPException(401, "Please sign in.")
    user = db.get_user_by_id(1)
    print("user @", user[4], ", required", level)
    if user[4] < level:
        raise HTTPException(
            401, "This user doesn't have the correct role to access this endpoint.")
    return user
