from typing import List
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, BackgroundTasks

import StatusManager as sm
import db
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
async def upload_file(upload: UploadFile, background_tasks: BackgroundTasks, user: db.User = Depends(standard_user)):
    if not upload.filename.endswith(".gcode"):
        raise HTTPException(
            status_code=400, detail="File must be a .gcode file")
    data = (await upload.read()).decode("utf-8")
    gcode_dir = os.path.join(config.files_location, str(user.id))
    if not os.path.exists(gcode_dir):
        os.mkdir(gcode_dir)
    path = os.path.join(gcode_dir, upload.filename)
    try:
        with open(path, "x+") as f:
            f.write(data)
    except FileExistsError:
        raise HTTPException(status_code=400, detail="File already exists.")
    job_id = db.jobs.add_job(path, -1, user.id)
    background_tasks.add_task(set_gcode_filament_length, data, job_id)
    return job_id


def set_gcode_filament_length(gcode: str, job_id: int):
    # NOTE: This was modelled off of Marlin flavor gcode from Dremel's outdated Cura fork
    # Will likely need modification for other printers since there's a lot of
    # commands I don't handle here
    length = 0.0
    lines = gcode.splitlines()
    current_sum = 0.0
    for line in lines:
        if line[0] == ";":
            # semicolons indicate a comment in a line.
            # we don't want to read those, so we skip it
            continue
        tokens = line.split(" ")
        token_idx = 0
        for token in tokens:
            if token == "G1":
                # this command controls the extruder's location and feed amount
                # the continue statement ensures that we keep going through the other tokens
                # to get the current amount of filament extruded
                token_idx += 1
                continue
            if token[0] == "E":
                # this token is found in the G1 command and denotes the current extrude amount
                # which is absolute by default (at least for Dremel's printers) unless reset with G92
                current_sum = float(token[1:])
                token_idx += 1
                break
            if token == "G92":
                # This command resets the current amount of filament extruded
                # so the next G1 command starts at 0 again
                # Not entirely sure why this reset is a thing, but
                # it seems to be run on different "sections" of the gcode
                # ex: switching to working on the support to the walls
                length += current_sum
                current_sum = 0
                token_idx += 1
                break
            if token == ";":
                token_idx += 1
                break
            if token_idx == 0:
                # at this point, if the command doesn't fall into one of the above conditions
                # the command isn't one we need to handle (ex: fans, temp changes, etc.)
                # so we skip the line
                break
            token_idx += 1
    length += current_sum
    print("Parsed gcode with length (mm)", length)
    db.jobs.update_job_filament_len(job_id, length)


@router.get("/{id}/history", dependencies=[Depends(logged_in)])
def get_job_history(job_id: int):
    return db.jobs.get_history_by_job_id(job_id)
