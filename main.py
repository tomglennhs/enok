from fastapi import FastAPI
import db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def read_root():
    users = db.getUsers()
    return {"Hello": users}

@app.on_event("shutdown")
def shutdown_event():
    db.con.close()