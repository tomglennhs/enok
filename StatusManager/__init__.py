import os
import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG)


sample_output = "{\"buildPlate_target_temperature\":60,\"chamber_temperature\":26,\"door_open\":0,\"elaspedtime\":0,\"error_code\":200,\"extruder_target_temperature\":0,\"fanSpeed\":0,\"filament_type \":\"PLA\",\"firmware_version\":\"v3.0_R02.11.17\",\"jobname\":\"45-pla-sword-sheath.gcode\",\"jobstatus\":\"preparing\",\"layer\":0,\"message\":\"success\",\"networkBuild\":0,\"platform_temperature\":58,\"progress\":0,\"remaining\":0,\"status\":\"busy\",\"temperature\":40,\"totalTime\":0}"


class StatusManager:
    def __init__(self):
        config = open("config.json", "r")
        json_config = config.read()
        config.close()
        config = json.loads(json_config)
        self.config = config

    def get_printer_status(self):
        for item in self.config["IP"]:
            if isinstance(item, str):
                req = requests.post("http://" + item + "/command", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data = {'data-urlencode': "GETPRINTERSTATUS="})
                return req
                


class PrinterDataHandler:
    def __init__(self):
        config = open("config.json", "r")
        json_config = config.read()
        config.close()
        config = json.loads(json_config)
        self.config = config

    def set_printer_data(self, *name):
        pass

    def get_printer_data(self):
        pass

    def purge_printer_data(self):
        pass

SM = StatusManager()
print(SM.get_printer_status())