from typing import Dict
from printers.base import PrinterStatus, BasePrinter
from db import printers
from multiprocessing import Pool

sample_output = "{\"buildPlate_target_temperature\":60,\"chamber_temperature\":26,\"door_open\":0,\"elaspedtime\":0," \
                "\"error_code\":200,\"extruder_target_temperature\":0,\"fanSpeed\":0,\"filament_type \":\"PLA\"," \
                "\"firmware_version\":\"v3.0_R02.11.17\",\"jobname\":\"45-pla-sword-sheath.gcode\"," \
                "\"jobstatus\":\"preparing\",\"layer\":0,\"message\":\"success\",\"networkBuild\":0," \
                "\"platform_temperature\":58,\"progress\":0,\"remaining\":0,\"status\":\"busy\",\"temperature\":40," \
                "\"totalTime\":0} "

state: Dict[int, PrinterStatus] = {}


def update_printer_status():
    ps = printers.get_printers()
    with Pool(5) as pool:
        statuses = pool.map(_map, ps)
    for status in statuses:
        state[status.printer_id] = status


def _map(printer: BasePrinter):
    return printer.printer_status()
