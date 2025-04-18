from datetime import datetime, timedelta

from app.core.config import settings

CREATE_DATE = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

CLOSE_DATE = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')

INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
FORMAT = '%Y/%m/%d %H:%M:%S'
ROW_COUNT = 100
COLUMN_COUNT = 11
SHEET_ID = 0
UPDATE_ROW = 30
UPDATE_COLUMN = 5