from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobFile(BaseModel):
    id: int
    filepath: str
    filament_length: float
    user_id: int


class Role(Enum):
    # Users that are not certified to use printers.
    VIEW_ONLY = 0
    # Users that are certified to use printers.
    STANDARD = 1
    # Users that have super-user privileges.
    ADMIN = 2


class User(BaseModel):
    id: int
    name: str
    email: str
    password: Optional[str]
    role: Role
    quota: float
    login_provider: str


class JobHistory(BaseModel):
    id: int
    time_started: str
    time_finished: str
    status: str
    job_file_id: int
    printer_id: int
