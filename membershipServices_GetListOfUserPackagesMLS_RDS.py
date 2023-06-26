from datetime import datetime
from realtyfeed.datasets import sample_response, json_to_dict
from realtyfeed.orm import RDSHandler
from realtyfeed.exceptions import (
    InvalidInputException,
    DatabaseException
)

from validator import validate_event
from get_data import get_membership_data



def lambda_handler(event, context):
    response = sample_response.copy()
    response['result'] = list()
    event = json_to_dict(event)

    # ---------- EVENT INPUT ----------
    try:
        event = event['body']
    except Exception as e:
        print(str(e))
        raise InvalidInputException(
            error_message='Error in event body',
            error_status_code="umc-05-001-01"
        )

    # ---------- VALIDATE INPUT ----------
    error_list = validate_event(event)
    if error_list:
        raise InvalidInputException(
            error_message=f"Invalid request body: {error_list}",
            error_status_code="umc-05-001-02"
        )

    # ---------- RDS Connection ----------
    try:
        rds_handler = RDSHandler(table_name="", is_cursor_dict=True)
        cursor = rds_handler.cursor
    except Exception as e:
        print(str(e))
        raise DatabaseException(
            error_status_code="umc-05-001-03"
        )

    data = get_membership_data(event, cursor)
    for obj in data:
        obj['start_date'] = obj['start_date'].isoformat() if isinstance(
            obj['start_date'], datetime) else obj['start_date']
        obj['end_date'] = obj['end_date'].isoformat() if isinstance(
            obj['end_date'], datetime) else obj['end_date']
        obj['cancellation_date'] = obj['cancellation_date'].isoformat() if isinstance(
            obj['cancellation_date'], datetime) else obj['cancellation_date']
        obj['period_start'] = obj['period_start'].isoformat() if isinstance(
            obj['period_start'], datetime) else obj['period_start']
        obj['period_end'] = obj['period_end'].isoformat() if isinstance(
            obj['period_end'], datetime) else obj['period_end']
        obj['membership_since'] = obj['membership_since'].isoformat() if isinstance(
            obj['membership_since'], datetime) else obj['membership_since']

    response['result'] = data

    rds_handler.close_connection()

    response['is_success'] = True
    return response

