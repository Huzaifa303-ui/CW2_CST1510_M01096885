import pandas as pd
from pathlib import Path
from app.data.db import connect_database


def insert_incident(id, title, severity, status, date):
    """Insert new incident."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (id, title, severity, status, date)
        VALUES (?, ?, ?, ?, ?)
    """, (id, title, severity, status, date))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id


def get_all_incidents():
    """Get all incidents as DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df



def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    
    TODO: Implement UPDATE operation.
    """
    # TODO: Write UPDATE SQL: UPDATE cyber_incidents SET status = ? WHERE id = ?
    update_sql = "UPDATE cyber_incidents SET status = ? WHERE id = ?"

    # TODO: Execute and commit
    cursor = conn.cursor()
    cursor.execute(update_sql, (new_status, incident_id))
    conn.commit()

    # TODO: Return cursor.rowcount
    updated_rows = cursor.rowcount
    print(f"Updated {updated_rows} incident(s) with ID {incident_id} to status '{new_status}'.")
    return updated_rows



def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    
    TODO: Implement DELETE operation.
    """
    # TODO: Write DELETE SQL: DELETE FROM cyber_incidents WHERE id = ?
    delete_sql = "DELETE FROM cyber_incidents WHERE id = ?"

    # TODO: Execute and commit
    cursor = conn.cursor()
    cursor.execute(delete_sql, (incident_id,))
    conn.commit()

    # TODO: Return cursor.rowcount
    deleted_rows = cursor.rowcount
    print(f"Deleted {deleted_rows} incident(s) with ID {incident_id}.")
    return deleted_rows


def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Uses: SELECT, FROM, GROUP BY, ORDER BY
    """
    query = """
    SELECT title, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY title
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df



def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Uses: SELECT, FROM, WHERE, GROUP BY, ORDER BY
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    return df



def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    Uses: SELECT, FROM, GROUP BY, HAVING, ORDER BY
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn, params=(min_count,))
    return df



def get_incidents_by_severity(conn, severity):
    """
    Retrieve incidents filtered by severity.

    Args:
        conn: Database connection
        severity: Severity level to filter by (e.g., 'High', 'Medium', 'Low')

    Returns:
        pandas.DataFrame: Filtered incidents
    """
    query = """
        SELECT id, title, severity, status, date
        FROM cyber_incidents
        WHERE severity = ?
    """
    df = pd.read_sql_query(query, conn, params=(severity,))
    return df



def get_incidents_by_status(conn, status):
    """
    Retrieve incidents filtered by status.

    Args:
        conn: Database connection
        status: Status to filter by (e.g., 'Open', 'Closed', 'In Progress')

    Returns:
        pandas.DataFrame: Filtered incidents
    """
    query = """
        SELECT id, title, severity, status, date
        FROM cyber_incidents
        WHERE status = ?
    """
    df = pd.read_sql_query(query, conn, params=(status,))
    return df

