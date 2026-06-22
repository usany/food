import requests

from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
from django.db.backends.sqlite3.creation import DatabaseCreation as SQLiteDatabaseCreation
from django.db.backends.sqlite3.introspection import DatabaseIntrospection as SQLiteDatabaseIntrospection
from django.db.backends.sqlite3.operations import DatabaseOperations as SQLiteDatabaseOperations
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor as SQLiteDatabaseSchemaEditor
from django.db.backends.sqlite3.features import DatabaseFeatures as SQLiteDatabaseFeatures
from django.db.backends.utils import CursorWrapper
from django.db.utils import OperationalError
from django.core.exceptions import ImproperlyConfigured


class D1RestCreation(SQLiteDatabaseCreation):
    def _create_test_db(self, verbosity, autoclobber, keepdb=False):
        return None


class D1RestIntrospection(SQLiteDatabaseIntrospection):
    pass


class D1RestOperations(SQLiteDatabaseOperations):
    def last_executed_query(self, cursor, sql, params):
        return sql


class D1RestSchemaEditor(SQLiteDatabaseSchemaEditor):
    pass


class D1RestFeatures(SQLiteDatabaseFeatures):
    can_return_columns_from_insert = False
    can_return_rows_from_bulk_insert = False
    supports_transactions = False
    supports_stddev = False
    supports_variance = False
    supports_explain_analyze = False
    can_introspect_foreign_keys = True
    supports_column_check_constraints = False


class D1RestCursorWrapper(CursorWrapper):
    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)


class D1RestConnection:
    def __init__(self, settings_dict):
        self.settings_dict = settings_dict
        self.account_id = settings_dict.get('CLOUDFLARE_ACCOUNT_ID', '').strip()
        self.database_id = settings_dict.get('CLOUDFLARE_DATABASE_ID', '').strip()
        self.token = settings_dict.get('CLOUDFLARE_TOKEN', '').strip()
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/d1/database/{self.database_id}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.queries_log = []
        self._queries_log = []
        self.in_atomic_block = False
        self.atomic_block_savepoint = None

    def _execute(self, sql, params=None):
        if params:
            sql = self._format_sql(sql, params)
        
        try:
            response = requests.post(
                f"{self.base_url}/query",
                headers=self.headers,
                json={"sql": sql},
                timeout=30,
            )
        except requests.RequestException as exc:
            raise OperationalError(f"D1 API request failed: {exc}") from exc
        
        if response.status_code != 200:
            raise OperationalError(self._format_d1_error(response))
        
        data = response.json()
        if not data.get("success"):
            errors = data.get("errors", [])
            messages = data.get("messages", [])
            error_msg = "; ".join([str(e) for e in errors + messages])
            raise OperationalError(f"D1 error: {error_msg}")
        
        results = data.get("result", [])
        return results

    def _format_d1_error(self, response):
        try:
            data = response.json()
        except ValueError:
            return f"D1 API error ({response.status_code}): {response.text}"

        errors = data.get("errors") or []
        error_codes = {error.get("code") for error in errors if isinstance(error, dict)}
        if response.status_code == 403 and 7403 in error_codes:
            return (
                "D1 API authorization failed (Cloudflare error 7403). "
                "Check that CFACCOUNTID is the account that owns CFDATABASEID and "
                "that CFAPITOKEN has Cloudflare D1 edit/read access for that account."
            )

        return f"D1 API error ({response.status_code}): {data}"

    def _format_sql(self, sql, params):
        if not params:
            return sql
        formatted = sql
        for param in params:
            if param is None:
                formatted = formatted.replace('%s', 'NULL', 1)
            elif isinstance(param, str):
                formatted = formatted.replace('%s', f"'{param.replace("'", "''")}'", 1)
            elif isinstance(param, (int, float)):
                formatted = formatted.replace('%s', str(param), 1)
            elif isinstance(param, bool):
                formatted = formatted.replace('%s', '1' if param else '0', 1)
            else:
                formatted = formatted.replace('%s', f"'{param}'", 1)
        return formatted

    def cursor(self):
        return D1RestCursor(self)

    def commit(self):
        pass

    def rollback(self):
        pass

    def close_if_unusable_or_obsolete(self):
        pass

    def close(self):
        pass

    def is_usable(self):
        try:
            self._execute("SELECT 1")
            return True
        except Exception:
            return False


class D1RestCursor:
    def __init__(self, connection):
        self.connection = connection
        self.description = None
        self.rowcount = -1
        self.arraysize = 1
        self._results = []
        self._index = 0

    def execute(self, sql, params=None):
        self.connection.queries_log.append({"sql": sql, "params": params, "time": 0})
        self._index = 0
        results = self.connection._execute(sql, params)
        self._results = results[0].get("results", []) if results else []
        self.rowcount = len(self._results)
        if self._results and isinstance(self._results[0], dict):
            self.description = [(k, None, None, None, None, None, None) for k in self._results[0].keys()]
        else:
            self.description = None
        return self

    def executemany(self, sql, param_list):
        for params in param_list:
            self.execute(sql, params)
        return self

    def fetchone(self):
        if self._index < len(self._results):
            row = self._results[self._index]
            self._index += 1
            return tuple(row.values()) if isinstance(row, dict) else row
        return None

    def fetchmany(self, size=None):
        size = size or self.arraysize
        rows = []
        while len(rows) < size and self._index < len(self._results):
            row = self._results[self._index]
            self._index += 1
            rows.append(tuple(row.values()) if isinstance(row, dict) else row)
        return rows

    def fetchall(self):
        rows = []
        while self._index < len(self._results):
            row = self._results[self._index]
            self._index += 1
            rows.append(tuple(row.values()) if isinstance(row, dict) else row)
        return rows

    def close(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row


class DatabaseWrapper(SQLiteDatabaseWrapper):
    vendor = "cloudflare_d1"
    display_name = "D1 (REST API)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features = D1RestFeatures(self)
        self.ops = D1RestOperations(self)
        self.creation = D1RestCreation(self)
        self.introspection = D1RestIntrospection(self)
        self.SchemaEditor = D1RestSchemaEditor

    def get_connection_params(self):
        settings_dict = self.settings_dict
        required = ['CLOUDFLARE_ACCOUNT_ID', 'CLOUDFLARE_DATABASE_ID', 'CLOUDFLARE_TOKEN']
        for key in required:
            if not settings_dict.get(key, '').strip():
                raise ImproperlyConfigured(f"settings.DATABASES['default']['{key}'] is required")
        return settings_dict

    def get_new_connection(self, conn_params):
        return D1RestConnection(conn_params)

    def init_connection_state(self):
        pass

    def create_cursor(self, name=None):
        return D1RestCursorWrapper(self.connection.cursor(), self)

    def _set_autocommit(self, autocommit):
        pass

    def is_usable(self):
        try:
            return self.connection.is_usable()
        except Exception:
            return False

    def check_constraints(self, table_names=None):
        pass
