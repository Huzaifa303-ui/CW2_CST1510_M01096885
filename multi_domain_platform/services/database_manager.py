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
 
 def create_security_incident(self, title, severity, status, date):
    sql = """
    INSERT INTO security_incidents (title, severity, status, date)
    VALUES (?, ?, ?, ?)
    """
    self.execute_query(sql, (title, severity, status, date))


 def update_security_incident(self, incident_id, severity, status):
    sql = """
    UPDATE security_incidents
    SET severity = ?, status = ?
    WHERE id = ?
    """
    self.execute_query(sql, (severity, status, incident_id))


 def delete_security_incident(self, incident_id):
    sql = "DELETE FROM security_incidents WHERE id = ?"
    self.execute_query(sql, (incident_id,))



 def create_dataset_incident(self, name, source, category, size):
    sql = """
    INSERT INTO datasets_metadata (name, source, category, size)
    VALUES (?, ?, ?, ?)
    """
    self.execute_query(sql, (name, source, category, size))


 def update_dataset_incident(self, incident_id, source, category, size):
    sql = """
    UPDATE datasets_metadata
    SET source = ?, category = ?, size = ?
    WHERE id = ?
    """
    self.execute_query(sql, (source, category,size, incident_id))


 def delete_dataset_incident(self, incident_id):
    sql = "DELETE FROM datasets_metadata WHERE id = ?"
    self.execute_query(sql, (incident_id,))


 def create_ITticket(self, title, priority, status, created_date):
    sql = """
    INSERT INTO it_tickets (title, priority, status, created_date)
    VALUES (?, ?, ?, ?)
    """
    self.execute_query(sql, (title, priority, status, created_date))


 def update_ITticket(self, incident_id,priority, status):
    sql = """
    UPDATE it_tickets
    SET priority = ?, status = ?
    WHERE id = ?
    """
    self.execute_query(sql, (priority,status, incident_id))


 def delete_ITticket(self, incident_id):
    sql = "DELETE FROM it_tickets WHERE id = ?"
    self.execute_query(sql, (incident_id,))
        
