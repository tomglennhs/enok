import os
import requests
import json
import logging
import sqlite3
logging.basicConfig(level=logging.DEBUG)
con = sqlite3.connect('enok.db', check_same_thread=False)
cur = con.cursor()

sample_output = "{\"buildPlate_target_temperature\":60,\"chamber_temperature\":26,\"door_open\":0,\"elaspedtime\":0,\"error_code\":200,\"extruder_target_temperature\":0,\"fanSpeed\":0,\"filament_type \":\"PLA\",\"firmware_version\":\"v3.0_R02.11.17\",\"jobname\":\"45-pla-sword-sheath.gcode\",\"jobstatus\":\"preparing\",\"layer\":0,\"message\":\"success\",\"networkBuild\":0,\"platform_temperature\":58,\"progress\":0,\"remaining\":0,\"status\":\"busy\",\"temperature\":40,\"totalTime\":0}"


class StatusManager:
    def __init__(self):
        config = open("config.json", "r")
        json_config = config.read()
        config.close()
        config = json.loads(json_config)
        self.config = config

    def on_file_upload(gcode: str, queue):
        queue = json.loads(str(queue))
        try:
            queue["queue"].index(gcode)
            return "Print is already queued"
        except:
            queue["queue"].append(gcode)
            return json.dumps(queue)

    def can_start_print(self, UON):
        config = self.config
        if(not(self.config["PONO"]) or UON):
            return True
        else:
            return False

    def get_printer_status(self):
        ip = self.config["IP"]
        for i in ip:
            if isinstance(i, str):
                req = requests.post("http://" + i + "/command", headers={'Content-Type': 'application/x-www-form-urlencoded'}, data = {"GETPRINTERSTATUS":""})
                data = req.json()
                if data:
                    return data
                else:
                    raise Exception("Failed to get data from printer " + i)

