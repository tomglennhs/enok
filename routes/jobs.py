from fastapi import APIRouter, HTTPException, Query, UploadFile
import db
import StatusManager as sm
router = APIRouter(prefix="/jobs", tags=["jobs"])
from config import config

# TODO: implement
@router.get("/")
def list_jobs(all: bool = Query(False, description="List all uploaded jobs. Only for admins.")):
    return

@router.post("/")
def add_to_queue(file: str):
    queue = sm.StatusManager.on_file_upload(file, db.get_printer_param(id, 'queue'))
    db.set_queue(queue, id)
    return queue


@router.get("/jobs/{id}")
def get_job(id: str):
    job = db.get_job_file(id)
    if len(job) < 1:
        raise HTTPException(status_code=404, detail="Not found")
    return job

# TODO: implement
@router.delete("/{id}")
def delete_job(id: str):
    return

@router.post("/upload_file")
def upload_file(upload: UploadFile):
    if not upload.filename.endswith(".gcode"):
        return HTTPException(status_code=400, detail="File must be a .gcode file")
    user_id = "hi"
    file = open(f"{config.file_location}/{user_id}/{upload.filename}", "wb")
    file.write(upload.read())
    file.close()
    return