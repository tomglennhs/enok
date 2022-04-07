from typing import List
import os
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
import db
import StatusManager as sm
from config import config
from dependencies import standard_user

router = APIRouter(prefix="/jobs", tags=["jobs"])
state = sm.StatusManager()


@router.get("/")
def list_jobs(all: bool = Query(False, description="List all uploaded jobs. Only for admins."), user: db.User = Depends(standard_user)) -> List[db.JobFile]:
    if all:
        if user.role != db.Role.ADMIN:
            raise HTTPException(
                status_code=403, detail="Only admins can list all jobs.")
        return db.get_all_job_files()
    return db.get_job_files_by_user(user.id)


@router.post("/")
# TODO: move this to the printers
def add_to_queue(file: str, id: int):
    queue = state.on_file_upload(file, db.get_printer_param(id, 'queue'))
    db.set_queue(queue, id)
    return queue


@router.get("/{id}")
def get_job(id: str, user: db.User = Depends(standard_user)):
    job = db.get_job_file(id)
    return job


@router.delete("/{id}")
# TODO: implement
def delete_job(id: str, user: db.User = Depends(standard_user)):
    job = db.get_job_file(id)
    os.remove(job.filepath)
    db.delete_job(id)
    return


@router.post("/upload_file")
async def upload_file(upload: UploadFile, user: db.User = Depends(standard_user)):
    if not upload.filename.endswith(".gcode"):
        raise HTTPException(
            status_code=400, detail="File must be a .gcode file")
    data = (await upload.read()).decode("utf-8")
    length = get_gcode_filament_length(data)
    dir = os.path.join(config.files_location, str(user.id))
    if not os.path.exists(dir):
        os.mkdir(dir)
    path = os.path.join(dir, upload.filename)
    try:
        with open(path, "x") as f:
            f.write(data)
    except FileExistsError:
        raise HTTPException(status_code=400, detail="File already exists.")
    db.add_job(path, length, user.id)


def get_gcode_filament_length(gcode: str) -> float:
    # TODO: Implement
    lines = gcode.splitlines()
    for l in lines:
        pass
    return 0.0


@router.get("/{id}/history")
# TODO: implement
def get_job_history(id: str, user: db.User = Depends(standard_user)):
    return
