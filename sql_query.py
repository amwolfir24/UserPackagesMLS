"""
This module contains the function to 
generate SQL statements.
"""

from psycopg2 import sql
from sql_filter import filter_query


def query_maker(input: dict) -> sql.SQL:
    """
    To generate SQL statements based on input
    input: 
        {
            "AND": {
                "package_id__gte": "100"
            },
            "OR": {
                "package_name__like": "a" 
            }
        }
        or
        {
            "ALL": "True"
        }
    """
    and_conditions = list()
    or_conditions = list()
    conditions = None

    orderby = input.get('ORDERBY', "user_id")
    asc = input.get('ASC', 'true')
    orient = str()

    limit = str(int(input.get('LIMIT', "10")))
    offset = str(int(input.get('OFFSET', "0")))

    if asc == 'true':
        orient = 'ASC'
    else:
        orient = 'DESC'

    if "ALL" in input:
        query = sql.SQL("SELECT * FROM membershipMV "
                        f"ORDER BY {orderby} {orient} "
                        f"LIMIT {limit} OFFSET {offset};")
        return query

    if "AND" in input:
        and_conditions.extend(filter_query(input['AND']))
        if and_conditions:
            and_conditions = sql.SQL(' AND ').join(and_conditions)

    if "OR" in input:
        or_conditions.extend(filter_query(input['OR']))
        if or_conditions:
            or_conditions = sql.SQL(' OR ').join(or_conditions)

    if and_conditions and or_conditions:
        conditions = sql.SQL(' OR ').join([and_conditions, or_conditions])

    elif and_conditions:
        conditions = and_conditions

    elif or_conditions:
        conditions = or_conditions

    query = sql.SQL("SELECT * FROM membershipMV "
                    "WHERE {conditions} "
                    f"ORDER BY {orderby} {orient} "
                    f"LIMIT {limit} OFFSET {offset};").format(
        conditions=conditions
    )

    return query
