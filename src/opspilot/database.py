import sqlite3
from typing import Iterator
from .config import settings
from .storage.migrations import run_migrations
from pathlib import Path


def get_conn(db_path: str | None = None):
    path = db_path or settings.DB_PATH
    db_file = Path(path)
    if not db_file.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)
        run_migrations(path)
    else:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
            if cur.fetchone() is None:
                run_migrations(path)
        finally:
            conn.close()
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def with_conn(db_path: str | None = None):
    def _get():
        conn = get_conn(db_path)
        try:
            yield conn
        finally:
            conn.close()
    return _get
