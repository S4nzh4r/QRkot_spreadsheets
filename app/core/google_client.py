from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.services.constants import INFO


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
