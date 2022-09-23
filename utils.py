import json
from typing import Union
import ast


def read_json(filename: str, encoding: str = "utf-8") -> Union[list, dict]:
    with open(filename, encoding=encoding) as f:
        return json.load(f)


def bytes_to_dict(bytes_type_var: bytes):
    str_var = bytes_type_var.decode('utf-8')
    return ast.literal_eval(str_var)
