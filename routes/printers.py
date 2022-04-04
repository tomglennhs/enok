from fastapi import APIRouter, Depends
import db
from dependencies import admin_user, logged_in, standard_user
router = APIRouter(prefix="/printers", tags=["printers"])


@router.post("/{id}/queue")
# Will immediately start print if none in queue
def add_file_to_queue(id, user: db.User = Depends(standard_user)):
    return


@router.post("/{id}/pause")
def pause_current_print(id, user: db.User = Depends(standard_user)):
    return


@router.post("/{id}/resume")
def resume_current_print(id, user: db.User = Depends(standard_user)):
    return


@router.post("/{id}/stop")
def stop_current_print(id, user: db.User = Depends(standard_user)):
    return


@router.post("/{id}/next")
def start_next_in_queue(id, user: db.User = Depends(standard_user)):
    return


@router.get("/")
def get_printers(user: db.User = Depends(logged_in)):
    return


@router.get("/{id}")
def get_printer(id: str, user: db.User = Depends(logged_in)):
    return


@router.post("/", tags=["admin"])
def add_printer(user: db.User = Depends(admin_user)):
    return


@router.delete("/{id}", tags=["admin"])
def delete_printer(id: str, user: db.User = Depends(admin_user)):
    return


@router.patch("/{id}/queue", tags=["admin"])
def reorder_queue_item(id: str, old_index: int, new_index: int, user: db.User = Depends(admin_user)):
    return


@router.delete("/{id}/queue/{index}")
def remove_queue_item(id: str, index: int, user: db.User = Depends(admin_user)):
    return
