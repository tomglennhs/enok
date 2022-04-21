from fastapi import Response, Request, Form, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token

import db.users
from config import config
import db
import store
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google")
def login_google(response: Response, request: Request, g_csrf_token: str = Form(""), credential: str = Form("")):
    if not config.googleClientID:
        raise HTTPException(400, "Google login is not enabled.")
    csrf_token_cookie = request.cookies.get("g_csrf_token")
    if not csrf_token_cookie:
        raise HTTPException(400, "No CSRF token in Cookie.")
    if not g_csrf_token:
        raise HTTPException(400, "No CSRF token in post body.")
    if csrf_token_cookie != g_csrf_token:
        raise HTTPException(400, 'Failed to verify double submit cookie.')

    idinfo = id_token.verify_oauth2_token(
        credential, requests.Request(), config.googleClientID)

    if len(config.allowedDomains) > 0 and (
            "hd" not in idinfo.keys() or idinfo['hd'] not in config.allowedDomains):
        raise HTTPException(
            401, "Invalid email domain. Try signing in with your school email.")

    user = db.users.get_user_by_email(idinfo["email"])
    if user is None:
        user = db.users.create_user(idinfo["name"], idinfo["email"], "google")
    uid = user.id
    sid = uuid.uuid4()
    delta = timedelta(**config.sessionTimeout.dict())
    expires = datetime.now() + delta
    store.set(f"sessions/{sid}", {"uid": uid, "expires": expires})
    response.set_cookie("enok_sid", str(sid), httponly=True, secure=not config.dev,
                        max_age=int(delta.total_seconds()))
    return RedirectResponse(config.host)


@router.get("/logout")
def log_out(request: Request, response: Response):
    store.safeDelete(f"sessions/{request.cookies.get('enok_sid')}")
    response.set_cookie("enok_sid", "", max_age=-1)
    return
