import json
from typing import List, Optional

from pydantic import BaseModel

_file = open("config.json", "r")
_json_config = _file.read()
_file.close()

class Config(BaseModel):
    printerCheckFrequency: int
    IP: List[str]
    googleClientID: Optional[str]
    allowedDomains: List[str]
    # TODO: Type this better lol
    sessionTimeout: object
    dev: Optional[bool]
    host: str
    files_location: str
    
config = Config(**json.loads(_json_config))