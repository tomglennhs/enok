from fastapi import APIRouter, Query, UploadFile

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
