# https://docs.google.com/document/d/1Of4ZUU13UWfF1-2vZIfyzsz1yCOvCj9v9FT0aroKhuU/edit

from printers.base import BasePrinter
import requests
import os


class Dremel(BasePrinter):

    def upload_print(self, gcode_path: str):
        files = {
            "print_file": (os.path.split(gcode_path)[1], open(gcode_path, 'rb'))
        }
        print(files)
        req = requests.post("http://"+self.ip +
                            "/print_file_uploads", files=files)
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def start_print(self, file_name: str):
        req = requests.post("http://"+self.ip+"/command", data={
            "PRINT": file_name
        })
        print(req.text)
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def pause_print(self):
        req = requests.post("http://"+self.ip+"/command", data={
            "PAUSE": self._get_current_file_name()
        })
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def resume_print(self):
        # According to the gdoc, the command for resuming a paused print is the same as starting a new print
        return self.start_print(self._get_current_file_name())

    def cancel_print(self):
        req = requests.post("http://"+self.ip+"/command", data={
            "CANCEL": self._get_current_file_name()
        })
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def _get_current_file_name(self):
        req = requests.post("http://" + self.ip + "/command", headers={
                            'Content-Type': 'application/x-www-form-urlencoded'}, data={"GETPRINTERSTATUS": ""})
        data = req.json()
        if data:
            return data["jobname"]
