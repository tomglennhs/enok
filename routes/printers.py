from fastapi import APIRouter
import db
import StatusManager as sm

state = sm.StatusManager()
router = APIRouter(prefix="/printers", tags=["printers"])


@router.post("/{id}/queue")
# Will immediately start print if none in queue
def add_file_to_queue(id):
    return


@router.post("/{id}/pause")
def pause_current_print(id):
    return


@router.post("/{id}/resume")
def resume_current_print(id):
    return


@router.post("/{id}/stop")
def stop_current_print(id):
    return


@router.get("/{id}/next")
def start_next_in_queue(id):
    return state.can_start_print("USB")


@router.get("/")
def get_printers():
    return


@router.get("/{id}")
def get_printer(id: str):
    return


@router.post("/", tags=["admin"])
def add_printer():
    return


@router.delete("/{id}", tags=["admin"])
def delete_printer(id: str):
    return


@router.patch("/{id}/queue", tags=["admin"])
def reorder_queue_item(id: str, old_index: int, new_index: int):
    return


@router.delete("/{id}/queue/{index}")
def remove_queue_item(id: str, index: int):
    return
