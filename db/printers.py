from typing import List

from db import cur, con
from printers import base, dremel


def get_printer_by_id(printer_id: int) -> base.BasePrinter:
    printer = cur.execute("SELECT id, name, printer_host, camera, type, queue FROM printers WHERE id = ?", (printer_id,)).fetchone()
    printer_id, name, ip, camera, printer_type, queue = printer
    if printer_type == base.PrinterType.Dremel.value:
        return dremel.Dremel(id=printer_id, name=name, type=printer_type, queue=queue, camera=camera,
                             upload_method="Network", printer_host=ip)
    else:
        return NotImplemented


def get_printers() -> List[base.BasePrinter]:
    printers: List[base.BasePrinter] = []
    printer_list = cur.execute("SELECT id, name, printer_host, camera, type, queue FROM printers").fetchall()
    for printer in printer_list:
        printer_id, name, printer_host, camera, printer_type, queue = printer
        if printer_type == base.PrinterType.Dremel.value:
            printers.append(
                dremel.Dremel(id=printer_id, name=name, type=printer_type, printer_host=printer_host, queue=queue,
                              upload_method="Network", camera=camera))
    return printers


def delete_printer(printer_id: int):
    cur.execute("DELETE FROM printers WHERE id = ?", (printer_id,))
    con.commit()


def create_printer(name: str, printer_type: base.PrinterType, printer_host: str, upload_method: str, queue: str, camera: str = ""):
    cur.execute('''INSERT INTO printers (name, type, printer_host, queue, upload_method, camera) VALUES (?, ?, ?, ?, ?, ?)''',
                (name, printer_type.value, printer_host, queue, upload_method, camera))
    con.commit()
    return get_printer_by_id(cur.lastrowid)


def set_queue(queue: str, printer_id: int):
    # TODO: Better types for the queue - only serialize the queue as text when getting/setting it
    cur.execute("UPDATE printers SET queue = ? WHERE id = ?", (queue, printer_id))
    con.commit()

