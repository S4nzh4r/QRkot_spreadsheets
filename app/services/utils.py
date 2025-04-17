from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from app.services.constants import (
    COLUMN_COUNT, FORMAT, ROW_COUNT,
    SHEET_ID, UPDATE_COLUMN, UPDATE_ROW
)


async def get_now_date_time() -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    return now_date_time


async def get_body_spreadsheet() -> dict:
    current_time = await get_now_date_time()
    spreadsheet_body = {
        'properties': {'title': f'Отчёт на {current_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {
            'sheetType': 'GRID',
            'sheetId': SHEET_ID,
            'title': 'Лист1',
            'gridProperties': {'rowCount': ROW_COUNT,
                               'columnCount': COLUMN_COUNT}
        }}]
    }
    return spreadsheet_body


async def check_update_values(
        rows: Optional[int] = None,
        columns: Optional[int] = None
) -> None:
    if rows is not None:
        if rows > UPDATE_ROW and UPDATE_ROW > ROW_COUNT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Неверное количество строк в таблице'
            )

    if columns is not None:
        if columns > UPDATE_COLUMN and UPDATE_COLUMN > COLUMN_COUNT:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Неверное количество колонок в таблице'
            )


async def get_table_values(projects: list) -> list:
    current_time = await get_now_date_time()
    table_values = [
        ['Отчёт от', current_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    await check_update_values(rows=len(projects))

    for project in projects:
        # Тут я не уверен, что нужно проверять количество колонок
        await check_update_values(columns=len(project.keys()))
        new_row = [
            project['name'],
            project['duration'],
            project['description']
        ]
        table_values.append(new_row)
    return table_values
