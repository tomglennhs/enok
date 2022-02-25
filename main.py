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


@app.on_event("shutdown")
def shutdown_event():
    db.con.close()


@app.on_event("startup")
def startup_event():
    # StatusManager = sm.StatusManager
    # print(StatusManager)
    pass
  
# WIP
@app.on_event("startup")
def startup_event():
    state = sm.StatusManager()

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
