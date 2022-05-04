from PIL import Image
from io import BytesIO, StringIO
import json
import os
from abc import ABC
from typing import List
import cv2
from pydantic import Field

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
import cameras

import status as sm
import db
import db.jobs
from db.models import Role
import db.printers
import db.users
from dependencies import admin_user, logged_in, standard_user
from printers.base import BasePrinter, CurrentStatus, PrinterStatus

router = APIRouter(prefix="/printers", tags=["printers"])


@router.post("/{printer_id}/pause")
def pause_current_print(printer_id: int, user: db.User = Depends(standard_user)):
    db.printers.get_printer_by_id(printer_id).pause_print()
    return


@router.post("/{printer_id}/resume")
def resume_current_print(printer_id: int, user: db.User = Depends(standard_user)):
    db.printers.get_printer_by_id(printer_id).resume_print()
    return


@router.post("/{printer_id}/stop")
def stop_current_print(printer_id: int, user: db.User = Depends(standard_user)):
    # should we return people's quota back? dremel's api will at least tell us what layer we're on, so we can do some
    # gcode parsing to figure out how much filament we need to return
    db.printers.get_printer_by_id(printer_id).cancel_print()
    return


@router.get("/{printer_id}/next")
def start_next_in_queue(printer_id: int):
    printer = db.printers.get_printer_by_id(printer_id)
    queue = json.loads(printer.queue)["queue"]
    if len(queue) == 0:
        raise HTTPException(status_code=400, detail="No files in queue")
    status = sm.state[printer_id]
    if status.current_status != CurrentStatus.ReadyToPrint:
        raise HTTPException(status_code=400, detail="Not able to print")
    job = db.jobs.get_job_file(queue.pop(0)[0])
    printer.upload_print(job.filepath)
    printer.start_print(os.path.split(job.filepath)[1])


@router.get("/{printer_id}/camera/jpg", response_class=StreamingResponse)
def get_printer_frame(printer_id: int):
    try:
        frame = cameras.get_frame(printer_id)
    except KeyError:
        raise HTTPException(400)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frameRGB)

    tmpFile = BytesIO()
    img.save(tmpFile, "JPEG")

    def stream():
        tmpFile.seek(0)
        yield from tmpFile

    return StreamingResponse(content=stream(), media_type="image/jpeg")


@router.get("/status")
def get_all_printer_status(user: db.User = Depends(logged_in)) -> List[PrinterStatus]:
    arr = []
    printers = db.printers.get_printers()
    for printer in printers:
        arr.append(get_printer_status(printer.id))
    return arr


@router.get("/status/{printer_id}")
def get_printer_status(printer_id: int, user: db.User = Depends(logged_in)) -> PrinterStatus:
    status: sm.ExtendedPrinterStatus = sm.state[printer_id]
    update = False
    if status is None:
        printer = db.printers.get_printer_by_id(printer_id)
        status = sm.ExtendedPrinterStatus(
            **printer.printer_status().dict(), printer=printer)
        update = True
    if update:
        sm.state[printer_id] = status
    return status


@router.get("/")
def get_printers(user: db.User = Depends(logged_in)):
    return db.printers.get_printers()


@router.get("/{printer_id}")
def get_printer(printer_id: int, user: db.User = Depends(logged_in)):
    return db.printers.get_printer_by_id(printer_id)


# TODO: Figure out if there is a better way to make a model that inherits most properties from another but excludes some
class NewPrinter(BasePrinter, ABC):
    id: str = Field(None)

    def upload_print(self, gcode_path: str):
        return False

    def start_print(self, file_name: str):
        return False

    def cancel_print(self):
        return False

    def pause_print(self):
        return False

    def can_print(self):
        return False

    def resume_print(self):
        return False

    def printer_status(self):
        return


@router.post("/", tags=["admin"])
def add_printer(printer: NewPrinter, user: db.User = Depends(admin_user)):
    return db.printers.create_printer(name=printer.name, printer_type=printer.type, printer_host=printer.printer_host, camera=printer.camera, queue=printer.queue, upload_method=printer.upload_method)


@router.delete("/{printer_id}", tags=["admin"])
def delete_printer(printer_id: int, user: db.User = Depends(admin_user)):
    db.printers.delete_printer(printer_id)


@router.post("/{printer_id}/queue")
def add_file_to_queue(printer_id: int, job_id: int, user: db.User = Depends(standard_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    job = db.jobs.get_job_file(job_id)
    if job.filament_length == -1:
        raise HTTPException(400, "This job's filament length is being calculated, try again later.")
    new_quota = user.quota - job.filament_length
    if new_quota < 0:
        raise HTTPException(
            status_code=400, detail="Not enough quota")
    db.users.update_user_quota(user.id, new_quota)
    queue = json.loads(printer.queue)
    queue["queue"].append(
        [job_id, {"UploadMethod": "Network", "Owner": user.id}])
    db.printers.set_queue(queue, printer_id)
    return


@router.patch("/{printer_id}/queue", tags=["admin"])
def reorder_queue_item(printer_id: int, old_index: int, new_index: int, user: db.User = Depends(admin_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    queue = json.loads(printer.queue)
    queue["queue"].insert(new_index, queue["queue"].pop(old_index))
    db.printers.set_queue(queue, printer_id)
    return


@router.delete("/{printer_id}/queue/{index}")
def remove_queue_item(printer_id: int, index: int, user: db.User = Depends(standard_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    queue = json.loads(printer.queue)
    job_owner_id = queue["queue"][index][1]["Owner"]
    actor_is_owner = job_owner_id == user.id
    job_id = queue["queue"][index][0]
    if not actor_is_owner or user.role.value < Role.ADMIN.value:
        raise HTTPException(
            status_code=400, detail="You do not own this file")
    queue["queue"].pop(index)
    db.printers.set_queue(queue, printer_id)
    old_quota = user.quota if actor_is_owner else db.users.get_user_by_id(
        job_owner_id).quota
    job = db.jobs.get_job_file(job_id)
    db.users.update_user_quota(job_owner_id, old_quota + job.filament_length)
