from fastapi import Depends, HTTPException, Response, Cookie
import store
import datetime
import db

def logged_in(response: Response, enok_sid: str = Cookie(None)):
    print(enok_sid)
    if enok_sid == None:
        raise HTTPException(403, "Please sign in.")
    key = f"sessions/{enok_sid}"
    session = store.get(key)
    if session == None or session["expires"] < datetime.now():
        response.set_cookie("enok_sid", enok_sid, max_age=-1)
        store.safeDelete(key)
        raise HTTPException(403, "Your session has expired, please sign in again.")
    user = db.get_user_by_id(session["uid"])
    print(user)
    return user

def standard_user(current_user: db.User = Depends(logged_in)):
    if current_user.role <= db.Role.STANDARD:
        raise HTTPException(403, "You do not have permission to access this resource.")
    return current_user

def admin_user(current_user: db.User = Depends(logged_in)):
    if current_user.role <= db.Role.ADMIN:
        raise HTTPException(403, "You do not have permission to access this resource.")
    return current_user