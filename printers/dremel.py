# https://docs.google.com/document/d/1Of4ZUU13UWfF1-2vZIfyzsz1yCOvCj9v9FT0aroKhuU/edit

from datetime import datetime
from printers.base import BasePrinter, CurrentStatus, Duration, PrinterStatus, Temperature
import requests
import os


class Dremel(BasePrinter):

    def upload_print(self, gcode_path: str):
        files = {
            "print_file": (os.path.split(gcode_path)[1], open(gcode_path, 'rb'))
        }
        print(files)
        req = requests.post(self.printer_host +
                            "/print_file_uploads", files=files)
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def start_print(self, file_name: str):
        req = requests.post(self.printer_host + "/command", data={
            "PRINT": file_name
        })
        print(req.text)
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def pause_print(self):
        req = requests.post(self.printer_host + "/command", data={
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
        req = requests.post(self.printer_host + "/command", data={
            "CANCEL": self._get_current_file_name()
        })
        res = req.json()
        if res["message"] == "success":
            return True
        else:
            return False

    def _get_current_file_name(self) -> str:
        req = requests.post(self.printer_host + "/command", headers={
                            'Content-Type': 'application/x-www-form-urlencoded'}, data={"GETPRINTERSTATUS": ""})
        data = req.json()
        if data:
            return data["jobname"]

    def printer_status(self) -> PrinterStatus:
        req = requests.post(self.printer_host + "/command", headers={
                            'Content-Type': 'application/x-www-form-urlencoded'}, data={"GETPRINTERSTATUS": ""})
        data = req.json()
        bed = Temperature(target=data["buildPlate_target_temperature"], current=data["platform_temperature"])
        extruder = Temperature(target=data["extruder_target_temperature"], current=data["temperature"])
        chamber = Temperature(current=data["chamber_temperature"])
        # TODO: Figure out what the paused/printing jobstatus is like
        status = CurrentStatus.Unknown
        if data["status"] == "ready":
            status = CurrentStatus.ReadyToPrint
        elif data["jobstatus"] == "preparing":
            status = CurrentStatus.Preparing
        # elif data["jobstatus"] == "!pausing":
            # status = CurrentStatus.Printing
        
        # elaspedtime is not a typo 💀 that is how it is from the API
        duration = Duration(elapsed=data["elaspedtime"], total=data["totalTime"], remaining=data["remaining"])
        return PrinterStatus(printer_id=self.id, bed_temp=bed, extruder_temp=extruder, chamber_temp=chamber, current_status=status, file_name=data["jobname"], progress=data["progress"], duration=duration, raw=req.text, filament=data["filament_type"], last_fetched=datetime.now())