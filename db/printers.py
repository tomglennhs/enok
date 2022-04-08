from typing import List

from db import cur, con
from printers import base, dremel


def get_printer_by_id(id: int) -> base.BasePrinter:
    printer = cur.execute("SELECT id, name, ip, camera, type, queue FROM printers WHERE id = ?", (id,)).fetchone()
    id, name, ip, camera, type, queue = printer
    if type == base.PrinterType.Dremel.value:
        return dremel.Dremel(id=id, name=name, type=type, ip=ip, queue=queue, camera=camera, upload_method="Network")
    else:
        return NotImplemented


def get_printers() -> List[base.BasePrinter]:
    printers = []
    printer_list = cur.execute("SELECT id, name, ip, camera, type, queue FROM printers").fetchall()
    for printer in printer_list:
        id, name, ip, camera, type, queue = printer
        if type == base.PrinterType.Dremel.value:
            printers.append(
                dremel.Dremel(id=id, name=name, type=type, ip=ip, queue=queue, upload_method="Network", camera=camera))
    return printers


def delete_printer(id: int):
    cur.execute("DELETE FROM printers WHERE id = ?", (id,))
    con.commit()


def create_printer(name: str, type: base.PrinterType, ip: str, upload_method: str, queue: str):
    cur.execute('''INSERT INTO printers (name, type, ip, queue) VALUES (?, ?, ?, ?)''',
                (name, type, ip, queue, upload_method))
    con.commit()
    return get_printer_by_id(cur.lastrowid)


def set_queue(queue, id):
    cur.execute("UPDATE printers SET queue = ? WHERE id = ?", (queue, id))
    con.commit()


def get_printer_param(id, *param):
    print(param[0])
    if (len(param) == 1):
        return cur.execute("SELECT " + str(param[0]) +
                           " FROM printers WHERE ROWID = ?", (id,)).fetchone()[0]
    elif (len(param) > 1):
        printer_param = []
        for i in param:
            printer_param.append(cur.execute("SELECT " + str(i) +
                                             " FROM printers WHERE ROWID = ?", (id,)).fetchone())
        return printer_param
    else:
        return None