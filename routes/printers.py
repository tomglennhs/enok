import json
import os
from abc import ABC
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

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


@router.get("/")
def get_printers(user: db.User = Depends(logged_in)):
    return db.printers.get_printers()


@router.get("/{printer_id}")
def get_printer(printer_id: int, user: db.User = Depends(logged_in)):
    return db.printers.get_printer_by_id(printer_id)


@router.get("/{printer_id}/status")
def get_printer_status(printer_id: int, bg: BackgroundTasks, user: db.User = Depends(logged_in)) -> PrinterStatus:
    status = sm.state[printer_id]
    update = False
    if status is None:
        status = db.printers.get_printer_by_id(printer_id).printer_status()
        update = True
    if update:
        sm.state[printer_id] = status
    return status


@router.get("/status")
def get_all_printer_status(user: db.User = Depends(logged_in)) -> List[PrinterStatus]:
    arr = []
    printers = db.printers.get_printers()
    for printer in printers:
        arr.append(get_printer_status(printer.id))
    return arr


class NewPrinter(BasePrinter, ABC):
    id: str = None


@router.post("/", tags=["admin"])
def add_printer(printer: NewPrinter, user: db.User = Depends(admin_user)):
    return db.printers.create_printer(**printer.dict())


@router.delete("/{printer_id}", tags=["admin"])
def delete_printer(printer_id: int, user: db.User = Depends(admin_user)):
    db.printers.delete_printer(printer_id)


@router.post("/{printer_id}/queue")
def add_file_to_queue(printer_id: int, job_id: int, user: db.User = Depends(standard_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    job = db.jobs.get_job_file(job_id)
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
