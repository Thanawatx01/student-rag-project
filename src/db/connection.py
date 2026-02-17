from contextlib import contextmanager
from typing import Generator

import mysql.connector

import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[2]
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from config import settings

@contextmanager
def get_mysql_connection() -> Generator[mysql.connector.Connection, None, None]:
    conn = mysql.connector.connect(**settings.mysql_connection_dict)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
