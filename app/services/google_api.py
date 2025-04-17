from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services.constants import UPDATE_ROW, UPDATE_COLUMN
from app.services.utils import (
    get_body_spreadsheet, get_table_values
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:

    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = await get_body_spreadsheet()

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:

    service = await wrapper_services.discover('sheets', 'v4')

    table_values = await get_table_values(projects)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account( # noqa
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'Лист1!R1C1:R{UPDATE_ROW}C{UPDATE_COLUMN}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
