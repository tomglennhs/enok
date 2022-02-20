# https://docs.google.com/document/d/1Of4ZUU13UWfF1-2vZIfyzsz1yCOvCj9v9FT0aroKhuU/edit

from printers.printer import Printer
import requests

class Dremel(Printer):
    ip: str
    
    def __init__(self, ip):
        self.ip = ip
    
    def start_print(self,gcode_path: str):
        req = requests.post(self.ip+"/command", files={
            "PRINT": open(gcode_path,'rb')
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
        req = requests.post(self.ip+"/command", files={
            "PRINT": self._get_current_file_name()
        })
        if req.json().message == "success":
            return True
        else:
            return False
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
