from fastapi import APIRouter, Query, UploadFile
import db
import StatusManager as sm
router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/")
def list_jobs(all: bool = Query(False, description="List all uploaded jobs. Only for admins.")):
    return


@router.post("/")
def upload_job(file: UploadFile):
    return


@router.get("/jobs/{id}")
def get_job(id: str):
    return


@router.delete("/{id}")
def delete_job(id: str):
    return

#TODO make thise take in information from the front end JS scripts instead of being defined inside the function definition.
@router.get("/upload_file")
def upload_file(gcode = "file3.gcode", id = 1):
    queue = sm.StatusManager.on_file_upload(gcode, db.get_printer_param(id, 'queue'))
    db.set_queue(queue, id)
    return queue