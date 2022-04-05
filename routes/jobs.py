from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
import db
import StatusManager as sm
from config import config
from dependencies import standard_user

router = APIRouter(prefix="/jobs", tags=["jobs"])
state = sm.StatusManager()



# TODO: implement
@router.get("/")
def list_jobs(all: bool = Query(False, description="List all uploaded jobs. Only for admins."), user: db.User = Depends(standard_user)):
    return

@router.post("/")
def add_to_queue(file: str, id: int):
    queue = state.on_file_upload(file, db.get_printer_param(id, 'queue'))
    db.set_queue(queue, id)
    return queue


@router.get("/jobs/{id}")
def get_job(id: str, user: db.User = Depends(standard_user)):
    job = db.get_job_file(id)
    if len(job) < 1:
        raise HTTPException(status_code=404, detail="Not found")
    return job

# TODO: implement
@router.delete("/{id}")
def delete_job(id: str, user: db.User = Depends(standard_user)):
    return

@router.post("/upload_file")
def upload_file(upload: UploadFile, user: db.User = Depends(standard_user)):
    if not upload.filename.endswith(".gcode"):
        return HTTPException(status_code=400, detail="File must be a .gcode file")
    user_id = user.id
    file = open(f"{config.file_location}/{user_id}/{upload.filename}", "wb")
    file.write(upload.read())
    file.close()
    return

