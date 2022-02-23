from datetime import datetime
import uuid
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi import FastAPI, Form, Response, Request
from json import load, dump
import db
<<<<<<< Updated upstream
import store
=======
import StatusManager as sm

>>>>>>> Stashed changes
app = FastAPI()


# TODO: don't hardcode these here
GOOGLE_CLIENT_ID = "583695242034-fhr45p5p5bf996hm3ihmvfa5kg7g1e4t.apps.googleusercontent.com"
ALLOWED_EMAIL_DOMAINS = ["leanderisd.org", "k12.leanderisd.org"]
FRONTEND_HOST = "http://localhost:3000"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login/google")
def login_google(response: Response, request: Request, g_csrf_token: str = Form(""), credential: str = Form("")):
    csrf_token_cookie = request.cookies.get("g_csrf_token")
    print(g_csrf_token, csrf_token_cookie)
    if not csrf_token_cookie:
        response.status_code = 400
        return 'No CSRF token in Cookie.'
    if not g_csrf_token:
        response.status_code = 400
        return 'No CSRF token in post body.'
    if csrf_token_cookie != g_csrf_token:
        response.status_code = 400
        return 'Failed to verify double submit cookie.'

    idinfo = id_token.verify_oauth2_token(
        credential, requests.Request(), GOOGLE_CLIENT_ID)
    print(idinfo)

    if len(ALLOWED_EMAIL_DOMAINS) > 0 and ("hd" not in idinfo.keys() or idinfo['hd'] not in ALLOWED_EMAIL_DOMAINS):
        response.status_code = 401
        return "Invalid email domain. Try signing in with your school email."

    user = db.get_user_by_email(idinfo["email"])
    if (user == None):
        user = db.create_user(idinfo["name"], idinfo["email"], "google")
    uid = user[0]
    sid = uuid.uuid4()
    store.set(f"session.{sid}", {"uid": uid, "created": datetime.now()})
    response.set_cookie("sid", sid, httponly=True, secure=True)
    return RedirectResponse(FRONTEND_HOST)


# TODO: Create a @debug decorator so this only runs in dev
@app.get("/dev/store")
def read_store():
    return store.getAll()

@app.get("/users")
def read_root():
    users = db.get_table_data("users")
    return {"Hello": users}

@app.on_event("shutdown")
def shutdown_event():
    db.con.close()

@app.on_event("startup")
def startup_event():
    StatusManager = sm.StatusManager
    print(StatusManager)