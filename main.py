from enum import Enum
from datetime import datetime, timedelta
import uuid
from fastapi.responses import RedirectResponse
from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi import Cookie, FastAPI, Form, HTTPException, Query, Response, Request
import db
import store
import StatusManager as sm



app = FastAPI()
class Role(Enum):
    VIEW_ONLY = 0
    STANDARD = 1
    ADMIN = 2
import json

# Currently WIP
def auth_level(response: Response, enok_sid: str = Cookie(None), level: Role = 0):
    print(enok_sid)
    if enok_sid == None:
        raise HTTPException(401, "Please sign in")
    key = f"sessions/{enok_sid}"
    session = store.get(key)
    if session == None or session["expires"] < datetime.now():
        response.set_cookie("enok_sid", enok_sid, max_age=-1)
        store.safeDelete(key)
        raise HTTPException(401, "Please sign in")
    user = db.get_user_by_id(1)
    print("user @", user[4], ", required", level)
    if user[4] < level:
        raise HTTPException(401, "This user doesn't have the correct role to access this endpoint.")
    return user


config = open("config.json", "r")
json_config = config.read()
config.close()
config = json.loads(json_config)


GOOGLE_CLIENT_ID = config["googleClientID"]
ALLOWED_EMAIL_DOMAINS = config["allowedDomains"]
HOST = config["host"]
SESSION_EXPIRY_DELTA = timedelta(**config["sessionTimeout"])
DEV = config["dev"]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/login/google")
def login_google(response: Response, request: Request, g_csrf_token: str = Form(""), credential: str = Form("")):
    csrf_token_cookie = request.cookies.get("g_csrf_token")
    if not csrf_token_cookie:
        raise HTTPException(400, "No CSRF token in Cookie.")
    if not g_csrf_token:
        raise HTTPException(400, "No CSRF token in post body.")
    if csrf_token_cookie != g_csrf_token:
        raise HTTPException(400, 'Failed to verify double submit cookie.')

    idinfo = id_token.verify_oauth2_token(
        credential, requests.Request(), GOOGLE_CLIENT_ID)

    if len(ALLOWED_EMAIL_DOMAINS) > 0 and ("hd" not in idinfo.keys() or idinfo['hd'] not in ALLOWED_EMAIL_DOMAINS):
        raise HTTPException(
            401, "Invalid email domain. Try signing in with your school email.")

    user = db.get_user_by_email(idinfo["email"])
    if user == None:
        user = db.create_user(idinfo["name"], idinfo["email"], "google")
    uid = user[0]
    sid = uuid.uuid4()
    expires = datetime.now() + SESSION_EXPIRY_DELTA
    store.set(f"sessions/{sid}", {"uid": uid, "expires": expires})
    response.set_cookie("enok_sid", sid, httponly=True, secure=not DEV,
                        max_age=SESSION_EXPIRY_DELTA.total_seconds)
    return RedirectResponse(HOST)


def dev_only(next):
    def wrapper():
        if DEV == False:
            raise HTTPException(404)
        return next()
    return wrapper

# WIP
@app.on_event("startup")
def startup_event():
    state = sm.StatusManager()

@dev_only
@app.get("/login/dev")
def login_dev(response: Response, role: int = Query("2")):
    sid = uuid.uuid4()
    expires = datetime.now() + timedelta(days=7)
    store.set(f"sessions/{sid}", {"uid": "DEV", "expires": expires})
    response.set_cookie("enok_sid", sid, httponly=True, secure=not DEV,
                        max_age=SESSION_EXPIRY_DELTA.total_seconds)
    return "sup"

@app.get("/dev/store")
@dev_only
def read_store():
    return store.getAll()


@app.get("/users")
def read_root():
    users = db.get_table_data("users")
    return {"Hello": users}

#TODO make thise take in information from the front end JS scripts instead of being defined inside the function definition.
@app.get("/upload_file")
def upload_file(gcode = "file3.gcode", id = 1):
    queue = sm.StatusManager.on_file_upload(gcode, db.get_printer_param(id, 'queue'))
    db.set_queue(queue, id)
    return queue


@app.on_event("shutdown")
def shutdown_event():
    db.con.close()
