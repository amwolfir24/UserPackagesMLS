"""
This module contains all the required functions 
to generate SQL variables.
"""

import copy
from datetime import datetime
from validator import base_whitelist


def convert_type(input: dict) -> dict:
    """
    To convert the input type
    input sample: 
        {
            "package_name__eq": "mls1"
        }
    """
    for k, v in input.items():
        _type = base_whitelist[k.split('__')[0]]
        if _type == datetime:
            input[k] = datetime.strptime(v, '%Y/%m/%d')
        elif _type == bool:
            if v.lower() == 'true':
                input[k] = True
            elif v.lower() == 'false':
                input[k] = False
        elif _type == int:
            input[k] = str(int(v))
    return input


def convert_to_sql_var(input: dict) -> dict:
    """
    To convert the input to a valid SQL variable
    input sample: 
        {
            "package_name__eq": "mls1"
        }
    """
    for k, v in input.items():
        if k.endswith('__in') or k.endswith('__nin'):
            new_v = list()
            for item in v:
                new_v.append(convert_type({k: item})[k])
            input[k] = tuple(new_v)
        elif k.endswith('__like'):
            input[k] = '%{}%'.format(v)
        else:
            input[k] = convert_type({k: v})[k]
    return input


def vars_maker(input: dict) -> list:
    """
    To generate sql query variables
    """
    input_copy = copy.deepcopy(input)
    vars = list()

    if "AND" in input_copy:
        for k, v in input_copy['AND'].items():
            new_v = convert_to_sql_var({k: v})[k]
            vars.append(new_v)

    if "OR" in input_copy:
        for k, v in input_copy['OR'].items():
            new_v = convert_to_sql_var({k: v})[k]
            vars.append(new_v)

    return vars
