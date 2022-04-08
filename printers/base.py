import json
from abc import abstractmethod
from enum import Enum

from pydantic import BaseModel

empty_queue = {"queue": []}


class PrinterType(Enum):
    Dremel = "dremel"


class BasePrinter(BaseModel):
    id: int
    name: str
    type: PrinterType
    ip: str
    queue: str = json.dumps(empty_queue)
    upload_method: str
    camera: str

    @abstractmethod
    def upload_print(self, gcode_path: str) -> bool:
        pass

    @abstractmethod
    def start_print(self, file_name: str) -> bool:
        pass

    @abstractmethod
    def cancel_print(self) -> bool:
        pass

    @abstractmethod
    def pause_print(self) -> bool:
        pass

    @abstractmethod
    def resume_print(self) -> bool:
        pass
