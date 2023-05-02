import os
from contextlib import contextmanager
from dataclasses import dataclass
import os
import pymysql


@dataclass
class DBConnection:
    db: str
    user: str
    password: str
    host: str
    port: str


class WarehouseConnection:
    def __init__(self, db_conn: DBConnection):
        self.conn_url = pymysql.connect(
            host="db", user=db_conn.user, password=db_conn.password, database=db_conn.db,
            autocommit=True
        )

    @contextmanager
    def managed_cursor(self):
        self.curr = self.conn_url.cursor()
        try:
            yield self.curr
        finally:
            self.curr.close()
            

def get_warehouse_credentials() -> DBConnection:
    return DBConnection(
        db=os.getenv("MYSQL_DATABASE", ""),
        user='root',
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", ""),
        port=os.getenv("MYSQL_PORT", ""),
    )
