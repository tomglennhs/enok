from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Response, Cookie

import db
import db.users
import store
from config import config


async def logged_in(response: Response, enok_sid: str = Cookie(None)):
    expired = False
    if enok_sid is None:
        raise HTTPException(403, "Please sign in.")
    key = f"sessions/{enok_sid}"
    session = store.get(key)
    if session is None or session["expires"] < datetime.now():
        expired = True
        response.set_cookie("enok_sid", enok_sid, max_age=-1)
        store.safeDelete(key)
        raise HTTPException(403, "Your session has expired, please sign in again.")
    yield db.users.get_user_by_id(session["uid"])
    if not expired:
        session["expires"] = datetime.now() + timedelta(**config.sessionTimeout.dict())
        store.set(key, session)


def standard_user(current_user: db.User = Depends(logged_in)):
    if current_user.role.value < db.Role.STANDARD.value:
        raise HTTPException(403, "You do not have permission to access this resource.")
    return current_user


def admin_user(current_user: db.User = Depends(logged_in)):
    if current_user.role.value < db.Role.ADMIN.value:
        raise HTTPException(403, "You do not have permission to access this resource.")
    return current_user
