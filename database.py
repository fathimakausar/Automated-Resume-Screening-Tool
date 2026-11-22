"""SQLite helpers: connection, schema creation, audit log."""
import datetime as dt
import json
import sqlite3
from contextlib import contextmanager

import config


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


@contextmanager
def get_conn(db_path=None):
    path = db_path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db(db_path=None):
    with get_conn(db_path) as con:
        con.executescript(config.SCHEMA_FILE.read_text(encoding="utf-8"))


def audit(con, action, detail=""):
    con.execute("INSERT INTO audit_log(ts, action, detail) VALUES (?,?,?)", (now(), action, detail))


def loads(text, default=None):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return default
