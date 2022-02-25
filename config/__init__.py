import json

_file = open("config.json", "r")
_json_config = _file.read()
_file.close()

config = json.loads(_json_config)