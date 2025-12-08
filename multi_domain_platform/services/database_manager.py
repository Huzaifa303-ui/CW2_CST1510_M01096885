import sqlite3
import os
from typing import Any, Iterable
class DatabaseManager:
 """Handles SQLite database connections and queries."""
 def __init__(self, db_path=None):
        if db_path is None:
            self._db_path = r"C:\Users\User\VS code 1\multi_domain_platform\database\platform.db"
        else:
            self._db_path = os.path.abspath(db_path)

        self._connection = None

 def connect(self) -> None:
   if self._connection is None:
     self._connection = sqlite3.connect(self._db_path)
 
 def close(self) -> None:
   if self._connection is not None:
     self._connection.close()
     self._connection = None


 def execute_query(self, sql: str, params: Iterable[Any] = ()):
    """Execute a write query (INSERT, UPDATE, DELETE)."""
    if self._connection is None:
        self.connect()

    cur = self._connection.cursor()
    cur.execute(sql, tuple(params))
    self._connection.commit()
    return cur

 def fetch_one(self, sql: str, params: Iterable[Any] = ()):
   if self._connection is None:
     self.connect()
   cur = self._connection.cursor()
   cur.execute(sql, tuple(params))
   return cur.fetchone()
 
 def fetch_all(self, sql: str, params: Iterable[Any] = ()):
   if self._connection is None:
     self.connect()
   cur = self._connection.cursor()
   cur.execute(sql, tuple(params))
   return cur.fetchall()
        