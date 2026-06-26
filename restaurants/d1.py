import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings


class D1Error(RuntimeError):
    pass


def query_d1(sql, params=None):
    account_id = settings.CLOUDFLARE_ACCOUNT_ID
    database_id = settings.CLOUDFLARE_D1_DATABASE_ID
    api_token = settings.CLOUDFLARE_API_TOKEN

    missing = [
        name
        for name, value in {
            'CFACCOUNTID': account_id,
            'CFDBID or CFDATABASEID': database_id,
            'CFAPITOKEN or CFTOKEN': api_token,
        }.items()
        if not value
    ]
    if missing:
        raise D1Error(f"Missing Cloudflare D1 env vars: {', '.join(missing)}")

    url = (
        'https://api.cloudflare.com/client/v4/accounts/'
        f'{account_id}/d1/database/{database_id}/query'
    )
    payload = json.dumps({'sql': sql, 'params': params or []}).encode()
    request = Request(
        url,
        data=payload,
        method='POST',
        headers={
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode())
    except HTTPError as exc:
        body = exc.read().decode()
        raise D1Error(f'Cloudflare D1 HTTP {exc.code}: {body}') from exc
    except URLError as exc:
        raise D1Error(f'Cloudflare D1 request failed: {exc.reason}') from exc

    if not data.get('success'):
        raise D1Error(f"Cloudflare D1 query failed: {data.get('errors')}")

    return data.get('result', [])
