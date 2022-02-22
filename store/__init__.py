from typing import List

s = {}

def get(path: str):
    path = path.split(".")
    if len(path) == 1:
        return s.get(path[0], None)
    return _get(path[1:])

def _get(path: List[str]):
    if len(path) == 1:
        return s.get(path[0], None)
    return _get(path[1:])

def set(path: str, val: any):
    path = path.split(".")
    if len(path) == 1:
        s[path[0]] = val
        return
    _set(path[1:], val)

def _set(path: List[str], val: any):
    if len(path) == 1:
        s[path[0]] = val
        return
    _set(path[1:], val)

def delete(path: str):
    path = path.split(".")
    if len(path) == 1:
        del s[path[0]]
        return
    _delete(path[1:])

def _delete(path: List[str]):
    if len(path) == 1:
        del s[path[0]]
        return
    _delete(path[1:])

def deleteAll():
    s.clear()

def getAll():
    return s