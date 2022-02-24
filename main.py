from fastapi import FastAPI
import db
from routes import auth, dev
import StatusManager as sm

app = FastAPI()
app.include_router(auth.router)
app.include_router(dev.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("shutdown")
def shutdown_event():
    db.con.close()

@app.on_event("startup")
def startup_event():
    StatusManager = sm.StatusManager
    print(StatusManager)
    pass