"""
Input validation is paramount in programming as it serves 
as a crucial defense mechanism against potential security 
vulnerabilities and system failures. By validating user 
input, developers can ensure that only the expected and 
appropriate data is accepted by their programs. 
This helps prevent malicious activities like code injections, 
buffer overflows, and SQL injections, which can exploit 
vulnerabilities and compromise the integrity and confidentiality 
of systems. Furthermore, input validation helps maintain 
the stability and reliability of software by catching errors 
and preventing crashes caused by invalid or unexpected data. 
By diligently validating input, programmers can enhance the 
overall security and robustness of their applications, 
providing users with a safer and more reliable experience.

This module works as a validator for lambda input events. 
It just contains some rule-based functions, there is 
no specific business logic here to worry about. 
Some input white lists in each part do not necessarily 
mean they are of a type list. They are valid choices of 
the function input and may present as a 'set' type for ease of use.
"""

from datetime import datetime


base_whitelist = {
    "package_user_relation_id": int,
    "package_user_relation_status": str,
    "start_date": datetime,
    "end_date": datetime,
    "cancellation_date": datetime,
    "package_id": int,
    "package_type": int,
    "package_name": str,
    "package_active": bool,
    "package_source": str,
    "invoice_item_package_id": int,
    "invoice_item_package_status": int,
    "quantity": int,
    "promotion_id": int,
    "discount_id": int,
    "period_start": datetime,
    "period_end": datetime,
    "mls_access_customer_requests_id": int,
    "mls_access_customer_requests_status": str,
    "ticket_number": str,
    "user_id": int,
    "full_name": str,
    "username": str,
    "user_status": str,
    "email": str,
    "membership_since": datetime,
    "location": str,
}


filters = [
    '__eq',
    '__ne',
    '__gt',
    '__gte',
    '__lt',
    '__lte',
    '__in',
    '__nin',
    '__like'
]


def generate_input_whitelist_keys() -> list:
    """
    To generate input_whitelist_keys 
    """
    input_whitelist_keys = list()
    for item in list(base_whitelist.keys()):
        input_whitelist_keys.extend([
            item+_filter for _filter in filters])
    return input_whitelist_keys


def validate_string(input: str) -> list:
    """
    To validate input is a string and is not empty
    """
    error_list = list()
    if not isinstance(input, str):
        error_list = [f"'{input}' must be of type str!"]
    if input == "":
        error_list = [f"'{input}' should not be empty!"]
    return error_list


def validate_list_of_strings(input: list) -> list:
    """
    To validate input is a list and is not empty
    and that all list items are valid strings
    """
    error_list = list()
    if not isinstance(input, list):
        error_list = [f"'{input}' must be of type list!"]
        return error_list
    if input == []:
        error_list = [f"'{input}' should not be empty!"]
        return error_list
    for item in input:
        error_list.extend(validate_string(item))
    return error_list


def validate_dict(input: dict) -> list:
    """
    To validate input is a dictionary and is not empty
    """
    error_list = list()
    if not isinstance(input, dict):
        error_list = [f"'{input}' must be of type dict!"]
    if input == {}:
        error_list = [f"'{input}' should not be empty!"]
    return error_list


def validate_attribute_value(input: dict) -> list:
    """
    To validate attribute value
    input exp:
        {
            "name__eq": "mls1"
        }
    """
    error_list = list()

    for k, v in input.items():
        if isinstance(v, str):
            _type = base_whitelist[k.split('__')[0]]
            if _type == int and (not v.isdigit() or not int(v) > 0):
                error_list.append(
                    f"'{k}' must be a natural number in the string type!")
            elif _type == datetime:
                try:
                    datetime.strptime(v, '%Y/%m/%d')
                except:
                    error_list.append(
                        f"'{k}' must be in the correct datetime format(%Y/%m/%d)!")
            elif _type == bool and \
                    v.lower() not in ['true', 'false']:
                error_list.append(
                    f"'{k}'  must be in the correct bool format!")

    return error_list


def validate_operator(input: dict) -> list:
    """
    To validate operator attributes
    """
    error_list = list()

    error_list = validate_dict(input)
    if error_list:
        return error_list

    operator_whitelist = generate_input_whitelist_keys()

    if not set(input.keys()) <= set(operator_whitelist):
        error_list = [
            f"'AND/OR' only accepts this white list {operator_whitelist}"
        ]
        return error_list

    for k, v in input.items():
        if k.endswith('__in') or k.endswith('__nin'):
            error_list.extend(validate_list_of_strings(v))
            if isinstance(v, list):
                for item in v:
                    error_list.extend(validate_attribute_value({k: item}))
        else:
            error_list.extend(validate_string(v))
        error_list.extend(validate_attribute_value({k: v}))

    return error_list


def validate_event(event: dict) -> list:
    """
    To validate lambda input event 
    using all the above validators
    """
    error_list = list()

    event_white_list = [
        "AND",
        "OR",
        "ALL",
        "ORDERBY",
        "ASC",
        "LIMIT",
        "OFFSET"
    ]

    error_list = validate_dict(event)
    if error_list:
        return error_list

    if not set(event_white_list) & set(event.keys()):
        error_list = [
            f"Input must contain at least one of {event_white_list}!"]
        return error_list

    if ("AND" in event or "OR" in event) and \
            "ALL" in event:
        error_list = [
            "Input must contain one of 'ALL' and 'AND/OR'!"]
        return error_list

    if "ALL" in event:
        if not isinstance(event['ALL'], str):
            error_list = [
                "'ALL' must be of type str!"]
            return error_list
        if event['ALL'].lower() != "true":
            error_list = [
                "'ALL' only accepts true!"]
            return error_list

    if "AND" in event:
        error_list.extend(validate_operator(event['AND']))

    if "OR" in event:
        error_list.extend(validate_operator(event['OR']))

    if "ORDERBY" in event:
        if event['ORDERBY'] not in base_whitelist:
            error_list.append(
                f"'ORDERBY' only accepts this white list {list(base_whitelist.keys())}!")

    if "ASC" in event:
        if not isinstance(event['ASC'], str):
            error_list.append("'ASC' must be of type str!")
            return error_list
        if event['ASC'].lower() not in ['true', 'false']:
            error_list.append("'ASC' only accepts true and false!")

    if "LIMIT" in event:
        if not isinstance(event['LIMIT'], str) or \
            not event['LIMIT'].isdigit() or \
                not int(event['LIMIT']) > 0:
            error_list.append(
                "'LIMIT' must be a natural number in the string type!")

    if "OFFSET" in event:
        if not isinstance(event['OFFSET'], str) or \
                not event['OFFSET'].isdigit():
            error_list.append("'OFFSET' must be a number in the string type!")

    return list(set(error_list))