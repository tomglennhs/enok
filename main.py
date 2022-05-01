# TODO: Figure out ratelimiting
# TODO: Figure out pagination
# TODO: Is there anything important that I'm overlooking wrt to sessions?
# TODO: Handle errors better lol
import asyncio
import os
import cameras
import status

import uvicorn
from fastapi import FastAPI
import db
from config import config
from routes import auth, dev, printers, jobs

app = FastAPI(title="Enok")
app.include_router(auth.router)
app.include_router(dev.router)
app.include_router(printers.router)
app.include_router(jobs.router)


@app.get("/")
def read_root():
    return {"enok": app.version}


async def periodic(loop: asyncio.AbstractEventLoop):
    status.update_printer_status()
    cameras.on_state_update()
    cameras.loop()
    await asyncio.sleep(config.printerCheckFrequency)
    loop.create_task(periodic(loop))


@app.on_event("startup")
async def startup_event():
    if not os.path.exists(config.files_location):
        os.mkdir(config.files_location)
    loop = asyncio.get_running_loop()
    loop.create_task(periodic(loop))


@app.on_event("shutdown")
def shutdown_event():
    db.con.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
