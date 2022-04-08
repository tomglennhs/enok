from fastapi import APIRouter, Depends, HTTPException

import db.jobs
import db.printers
import db.users
from dependencies import admin_user, logged_in, standard_user
import db
import StatusManager as sm
from printers.base import BasePrinter
import json

state = sm.StatusManager()
router = APIRouter(prefix="/printers", tags=["printers"])


@router.post("/{id}/queue")
def add_file_to_queue(printer_id: int, job_id: int, user: db.User = Depends(standard_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    job = db.jobs.get_job_file(job_id)
    new_quota = user.quota - job.filament_length
    if new_quota < 0:
        raise HTTPException(
            status_code=400, detail="Not enough quota")
    db.users.update_user_quota(user.id, new_quota)
    queue = json.loads(printer.queue)
    queue["queue"].append([job_id, {"UploadMethod": "Network", "Owner": user.id}])
    db.printers.set_queue(queue, printer_id)
    return


@router.post("/{id}/pause")
def pause_current_print(printer_id, user: db.User = Depends(standard_user)):
    db.printers.get_printer_by_id(printer_id).pause_print()
    return


@router.post("/{id}/resume")
def resume_current_print(printer_id, user: db.User = Depends(standard_user)):
    db.printers.get_printer_by_id(printer_id).resume_print()
    return


@router.post("/{id}/stop")
def stop_current_print(printer_id, user: db.User = Depends(standard_user)):
    # should we return people's quota back? dremel's api will at least tell us what layer we're on, so we can do some
    # gcode parsing to figure out how much filament we need to return
    db.printers.get_printer_by_id(printer_id).cancel_print()
    return


# TODO: Implement
@router.get("/{id}/next")
def start_next_in_queue(id):
    if not state.can_start_print("USB"):
        raise HTTPException(
            status_code=400)
    printer = db.printers.get_printer_by_id(id)
    # if actively printing, fail
    # if nothing on queue, fail
    # if here, start print


@router.get("/")
def get_printers(user: db.User = Depends(logged_in)):
    return db.printers.get_printers()


@router.get("/{id}")
def get_printer(printer_id: int, user: db.User = Depends(logged_in)):
    return db.printers.get_printer_by_id(printer_id)


@router.post("/", tags=["admin"])
def add_printer(printer: BasePrinter, user: db.User = Depends(admin_user)):
    return db.printers.create_printer(**printer)


@router.delete("/{id}", tags=["admin"])
def delete_printer(printer_id: int, user: db.User = Depends(admin_user)):
    db.printers.delete_printer(printer_id)


@router.patch("/{id}/queue", tags=["admin"])
def reorder_queue_item(printer_id: int, old_index: int, new_index: int, user: db.User = Depends(admin_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    queue = json.loads(printer.queue)
    queue["queue"].insert(new_index, queue["queue"].pop(old_index))
    db.printers.set_queue(queue, printer_id)
    return


@router.delete("/{id}/queue/{index}")
def remove_queue_item(printer_id: int, index: int, user: db.User = Depends(admin_user)):
    printer = db.printers.get_printer_by_id(printer_id)
    queue = json.loads(printer.queue)
    queue["queue"].pop(index)
    db.printers.set_queue(queue, printer_id)
    return
