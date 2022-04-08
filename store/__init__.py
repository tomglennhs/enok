# TODO: Make this less sus

s = {}


def get(path: str):
    return s.get(path, None)


def set(path: str, val: any):
    s[path] = val


def delete(path: str):

    del s[path]


def safeDelete(path: str):
    try:
        delete(path)
    except KeyError:
        pass


def deleteAll():
    s.clear()


def getAll():
    return s
