"""
This module contains the function 
to get data of the materialized view 
using functions query_maker and vars_maker
and RDS cursor object
"""

from sql_query import query_maker
from sql_vars import vars_maker
from realtyfeed.exceptions import DatabaseException


def get_membership_data(input: dict, cursor) -> list:
    """
    To get data of materialized view 
    based on input filters 
    :params 
        input: 
            {
                "AND": {
                    "package_id__gte": "100"
                },
                "OR": {
                    "package_name__like": "ab" 
                }
            }
            or
            {
                "ALL": "True"
            }
        cursor: RDS cursor object
    """
    sql_statement = query_maker(input)
    if "ALL" in input:
        sql_args = None
    else:
        sql_args = vars_maker(input)
    try:
        cursor.execute(sql_statement, vars=sql_args)
        membership_data = cursor.fetchall()
        membership_data = [dict(record) for record in membership_data]
        return membership_data
    except Exception as e:
        print(str(e))
        raise DatabaseException(
            error_status_code='umc-05-001-04'
        )
