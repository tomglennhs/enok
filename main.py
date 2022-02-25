# TODO: Figure out ratelimiting
# TODO: Figure out pagination
# TODO: Is there anything important that I'm overlooking wrt to sessions?

from fastapi import FastAPI
import db
from routes import auth, dev, printers, jobs
import StatusManager as sm



app = FastAPI()
app.include_router(auth.router)
app.include_router(dev.router)
app.include_router(printers.router)
app.include_router(jobs.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# WIP
@app.on_event("startup")
def startup_event():
    state = sm.StatusManager()


@app.on_event("shutdown")
def shutdown_event():
    db.con.close()
