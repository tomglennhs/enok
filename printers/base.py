from datetime import datetime
import json
from abc import abstractmethod
from enum import Enum
from typing import Optional

from pydantic import AnyHttpUrl, BaseModel

empty_queue = {"queue": []}


class PrinterType(Enum):
    Dremel = "dremel"


class CurrentStatus(Enum):
    ReadyToPrint = "ready_to_print"
    Preparing = "preparing"
    Printing = "printing"
    Paused = "paused"
    Error = "error"
    Unknown = "unknown"


class Temperature(BaseModel):
    target: Optional[float] = None
    current: Optional[float] = None


class Duration(BaseModel):
    elapsed: Optional[float] = None
    total: Optional[float] = None
    remaining: Optional[float] = None


class PrinterStatus(BaseModel):
    printer_id: int
    bed_temp: Temperature
    extruder_temp: Temperature
    chamber_temp: Temperature
    current_status: CurrentStatus
    filament: str
    file_name: str
    progress: float
    duration: Duration
    raw: Optional[str]
    last_fetched: datetime


class BasePrinter(BaseModel):
    id: int
    name: str
    type: PrinterType
    printer_host: AnyHttpUrl
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
    def can_print(self) -> bool:
        pass

    @abstractmethod
    def resume_print(self) -> bool:
        pass

    @abstractmethod
    def printer_status(self) -> PrinterStatus:
        pass
