# https://docs.google.com/document/d/1Of4ZUU13UWfF1-2vZIfyzsz1yCOvCj9v9FT0aroKhuU/edit

from array import array
from printers.printer import Printer
import requests


class Dremel(Printer):
    ip: str

    def __init__(self, ip):
        self.ip = ip

    def upload_print(self, gcode_path: str):
        req = requests.post(self.ip+"/print_file_uploads", files={
            "print_file": open(gcode_path, 'rb')
        })
        if req.json().message == "success":
            return True
        else:
            return False

    def start_print(self, file_name: str):
        req = requests.post(self.ip+"/command", files={
            "PRINT": file_name
        })
        if req.json().message == "success":
            return True
        else:
            return False

    def pause_print(self):
        req = requests.post(self.ip+"/command", files={
            "PAUSE": self._get_current_file_name()
        })
        if req.json().message == "success":
            return True
        else:
            return False

    def resume_print(self):
        # According to the gdoc, the command for resuming a paused print is the same as starting a new print
        return self.start_print(self._get_current_file_name())

    def cancel_print(self):
        req = requests.post(self.ip+"/command", files={
            "CANCEL": self._get_current_file_name()
        })
        if req.json().message == "success":
            return True
        else:
            return False

    def _get_current_file_name(self) -> str:
        # TODO: Pull this from wherever the status manager ends up storing stuff
        return ""
