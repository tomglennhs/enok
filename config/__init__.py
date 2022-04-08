import json
from typing import List, Optional

from pydantic import BaseModel

with open("config.json", "r") as _file:
    _json_config = _file.read()

# datetime.timedelta
class Delta(BaseModel):
    microseconds: int = 0
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0
    weeks: int = 0


class Config(BaseModel):
    printerCheckFrequency: int
    IP: List[str]
    googleClientID: Optional[str]
    allowedDomains: Optional[List[str]]
    sessionTimeout: Delta = Delta(hours=1)
    dev: bool = False
    host: str
    files_location: str
    UploadVia: str
    # TODO: I set this to be an arbitrary number, make it actually reasonable later
    default_user_quota: float


config = Config(**json.loads(_json_config))
