"""
This module contains all the required functions 
to generate SQL WHERE clauses.
"""

from psycopg2 import sql


def filter_eq(attribute: str) -> list:
    """
    (=) Equal filtering
    """
    conditions = [
        sql.SQL(' = ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_ne(attribute: str) -> list:
    """
    (!=) Not equal filtering
    """
    conditions = [
        sql.SQL(' != ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_gt(attribute: str) -> list:
    """
    (>) Greater than filtering
    """
    conditions = [
        sql.SQL(' > ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_gte(attribute: str) -> list:
    """
    (>=) Greater than or equal filtering
    """
    conditions = [
        sql.SQL(' >= ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_lt(attribute: str) -> list:
    """
    (<) Less than filtering
    """
    conditions = [
        sql.SQL(' < ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_lte(attribute: str) -> list:
    """
    (<=) Less than or equal filtering
    """
    conditions = [
        sql.SQL(' <= ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_in(attribute: str) -> list:
    """
    (IN) if a value matches any value in a list
    """
    conditions = [
        sql.SQL(' IN ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_nin(attribute: str) -> list:
    """
    (NOT IN) if a value does not match any of the values in a list
    """
    conditions = [
        sql.SQL(' NOT IN ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_like(attribute: str) -> list:
    """
    (LIKE) if a value matches a pattern
    """
    conditions = [
        sql.SQL(' LIKE ').join([
            sql.Identifier(attribute), sql.Placeholder()
        ])
    ]
    return conditions


def filter_query(input: dict) -> list:
    """
    Main filter function
    input: 
        {
            'package_id__gte': 100,
            'invoice_item_package_status__in': 
            [
                "1",
                "2"
            ],
            ... 
        }
    """
    filters = list()
    for k, v in input.items():
        if k.endswith('__eq'):
            filters.extend(
                filter_eq(k.replace("__eq", "")))
        elif k.endswith('__ne'):
            filters.extend(
                filter_ne(k.replace("__ne", "")))
        elif k.endswith('__gt'):
            filters.extend(
                filter_gt(k.replace("__gt", "")))
        elif k.endswith('__gte'):
            filters.extend(
                filter_gte(k.replace("__gte", "")))
        elif k.endswith('__lt'):
            filters.extend(
                filter_lt(k.replace("__lt", "")))
        elif k.endswith('__lte'):
            filters.extend(
                filter_lte(k.replace("__lte", "")))
        elif k.endswith('__in'):
            filters.extend(
                filter_in(k.replace("__in", "")))
        elif k.endswith('__nin'):
            filters.extend(
                filter_nin(k.replace("__nin", "")))
        elif k.endswith('__like'):
            filters.extend(
                filter_like(k.replace("__like", "")))

    return filters
