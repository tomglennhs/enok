import os
import requests
from config import config
import logging
logging.basicConfig(level=logging.DEBUG)


sample_output = "{\"buildPlate_target_temperature\":60,\"chamber_temperature\":26,\"door_open\":0,\"elaspedtime\":0,\"error_code\":200,\"extruder_target_temperature\":0,\"fanSpeed\":0,\"filament_type \":\"PLA\",\"firmware_version\":\"v3.0_R02.11.17\",\"jobname\":\"45-pla-sword-sheath.gcode\",\"jobstatus\":\"preparing\",\"layer\":0,\"message\":\"success\",\"networkBuild\":0,\"platform_temperature\":58,\"progress\":0,\"remaining\":0,\"status\":\"busy\",\"temperature\":40,\"totalTime\":0}"


class StatusManager:
    def __init__(self):
        self.config = config

    def get_printer_status(self):
        for ip in self.config["IP"]:
            if isinstance(ip, str):
                req = requests.post("http://" + ip + "/command", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data = {"GETPRINTERSTATUS":""})
                data = req.json()
                if data:
                    return data
                else:
                    raise Exception("Failed to get data from printer " + ip)
                


class PrinterDataHandler:
    def __init__(self):
        self.config = config

    def set_printer_data(self, *name):
        pass

    def get_printer_data(self):
        pass

    def purge_printer_data(self):
        pass

SM = StatusManager()
print(SM.get_printer_status())