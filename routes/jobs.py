from typing import List
import os
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
import db
import StatusManager as sm
import db.jobs
from config import config
from dependencies import logged_in, standard_user

router = APIRouter(prefix="/jobs", tags=["jobs"])
state = sm.StatusManager()


@router.get("/")
def list_jobs(all: bool = Query(False, description="List all uploaded jobs. Only for admins."), user: db.User = Depends(standard_user)) -> List[db.JobFile]:
    if all:
        if user.role != db.Role.ADMIN:
            raise HTTPException(
                status_code=403, detail="Only admins can list all jobs.")
        return db.jobs.get_all_job_files()
    return db.jobs.get_job_files_by_user(user.id)


@router.get("/{id}")
def get_job(id: str, user: db.User = Depends(logged_in)):
    return db.jobs.get_job_file(id)


@router.delete("/{id}")
def delete_job(job_id: int, user: db.User = Depends(standard_user)):
    job = db.jobs.get_job_file(job_id)
    if user.id == job.user_id or user.role == db.Role.ADMIN:
        os.remove(job.filepath)
        db.jobs.delete_job(job_id)
    raise HTTPException(status_code=403, detail="You are not allowed to delete this job.")


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
    db.jobs.add_job(path, length, user.id)


def get_gcode_filament_length(gcode: str) -> float:
    # TODO: Implement
    lines = gcode.splitlines()
    for l in lines:
        pass
    return 0.0


@router.get("/{id}/history", dependencies=[Depends(logged_in)])
def get_job_history(job_id: int):
    return db.jobs.get_history_by_job_id(job_id)
