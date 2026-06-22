import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.core.exceptions import ImproperlyConfigured

from django_cf.db.base_engine import (
    CFDatabaseWrapper,
    CFResult,
    is_read_only_query,
    replace_date_trunc_in_sql,
)


class DatabaseWrapper(CFDatabaseWrapper):
    vendor = "cloudflare_d1_http"
    display_name = "D1 (HTTP)"

    def get_connection_params(self):
        settings_dict = self.settings_dict
        account_id = settings_dict.get("CLOUDFLARE_ACCOUNT_ID")
        database_id = settings_dict.get("CLOUDFLARE_DATABASE_ID")
        api_token = settings_dict.get("CLOUDFLARE_API_TOKEN")

        missing = [
            name
            for name, value in {
                "CLOUDFLARE_ACCOUNT_ID": account_id,
                "CLOUDFLARE_DATABASE_ID": database_id,
                "CLOUDFLARE_API_TOKEN": api_token,
            }.items()
            if not value
        ]
        if missing:
            raise ImproperlyConfigured(
                f"settings.DATABASES is improperly configured. "
                f"Missing: {', '.join(missing)}"
            )
        return {
            "account_id": account_id,
            "database_id": database_id,
            "api_token": api_token,
        }

    def get_new_connection(self, conn_params):
        self.account_id = conn_params["account_id"]
        self.database_id = conn_params["database_id"]
        self.api_token = conn_params["api_token"]
        return super().get_new_connection(conn_params)

    def run_query(self, query, params=None) -> CFResult:
        query = replace_date_trunc_in_sql(query)

        if params:
            query = query.replace("%s", "?")

        url = (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{self.account_id}/d1/database/{self.database_id}/query"
        )
        payload = json.dumps({"sql": query, "params": params or []}).encode()
        request = Request(
            url,
            data=payload,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode())
        except HTTPError as exc:
            body = exc.read().decode()
            raise Exception(f"Cloudflare D1 HTTP {exc.code}: {body}") from exc
        except URLError as exc:
            raise Exception(f"Cloudflare D1 request failed: {exc.reason}") from exc

        if not data.get("success"):
            raise Exception(
                f"Cloudflare D1 query failed: {data.get('errors')}"
            )

        results = data.get("result", [])

        rows = []
        rows_read = 0
        rows_written = 0
        last_row_id = None
        total_row_count = 0

        for stmt_result in results:
            if not stmt_result.get("success"):
                continue
            stmt_rows = stmt_result.get("results", [])
            meta = stmt_result.get("meta", {})
            rows_read += meta.get("rows_read", 0)
            rows_written += meta.get("rows_written", 0)
            total_row_count += len(stmt_rows)

            changed_db = meta.get("changed_db", False)
            if changed_db and meta.get("last_row_id") is not None:
                last_row_id = meta["last_row_id"]

            for row in stmt_rows:
                row_items = tuple(row.values())
                rows.append(row_items)

        result = CFResult(rows)
        if rows_written:
            result.set_rowcount(rows_written)
        else:
            result.set_rowcount(rows_read)
        if last_row_id is not None:
            result.set_lastrowid(last_row_id)

        return result

    def close(self):
        pass
