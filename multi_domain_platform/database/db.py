import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = "multi_domain_platform/database/platform.db"

# Ensure folder exists
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")


# Sample data
sample_incidents = [
    ("Phishing email reported", "High", "Open", "2025-12-01"),
    ("Ransomware detected on server", "Critical", "Investigating", "2025-12-02"),
    ("Failed login attempts from unknown IP", "Medium", "Resolved", "2025-12-03"),
    ("Sensitive data exposed in cloud storage", "Critical", "Open", "2025-12-04"),
    ("Website traffic spike due to bot attack", "High", "Mitigated", "2025-12-05"),
    ("Employee downloaded confidential files", "Medium", "Open", "2025-12-06"),
    ("SQL injection on web form", "High", "Resolved", "2025-12-06"),
    ("Fake email campaign reported", "Low", "Closed", "2025-12-05"),
    ("Trojan found in downloaded attachment", "Medium", "Open", "2025-12-04"),
    ("Employee manipulated to share credentials", "Low", "Investigating", "2025-12-03")
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


# Create security_incidents table
cur.execute("""
CREATE TABLE IF NOT EXISTS security_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cur.executemany("""
INSERT INTO security_incidents (title, severity, status, date)
VALUES (?, ?, ?, ?)
""", sample_incidents)

conn.commit()


print(f"{len(sample_incidents)} sample security incidents created!")


# Sample datasets
sample_datasets = [
    ("Customer Data", "Internal CRM", "Business", 1200),
    ("Network Logs", "Firewall", "Security", 4500),
    ("Sales Reports", "ERP System", "Business", 3200),
    ("Malware Samples", "VirusTotal", "Security", 800),
    ("User Feedback", "Survey Tool", "Business", 1500),
    ("Server Metrics", "Monitoring Tool", "IT", 2500),
    ("Marketing Campaigns", "Ad Platform", "Business", 1800),
    ("Phishing Emails", "Security Team", "Security", 600),
    ("Financial Transactions", "Bank API", "Finance", 5000),
    ("Product Inventory", "ERP System", "Business", 2200),
    ("Threat Intelligence", "Open Threat DB", "Security", 950),
    ("Application Logs", "App Server", "IT", 1700),
    ("Employee Records", "HR System", "Business", 1300),
    ("Access Logs", "VPN Gateway", "Security", 2100),
    ("Incident Reports", "Security Team", "Security", 1100),
    ("Website Analytics", "Google Analytics", "Business", 2400),
    ("IoT Device Data", "IoT Hub", "IT", 1900),
    ("Phishing URLs", "Threat DB", "Security", 700),
    ("Marketing Leads", "CRM System", "Business", 1600),
    ("Database Backups", "Backup Server", "IT", 4800)
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create datasets_metadata table
cur.execute("""
CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        source TEXT,
        category TEXT,
        size INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Optional: randomize created_at within last 30 days
for i in range(len(sample_datasets)):
    days_ago = random.randint(0, 30)
    date_created = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
    INSERT INTO datasets_metadata (name, source, category, size, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (*sample_datasets[i], date_created))

conn.commit()


# Sample IT tickets
sample_tickets = [
    ("Cannot connect to VPN", "High", "Open"),
    ("Laptop not booting", "Critical", "Investigating"),
    ("Email not syncing", "Medium", "Resolved"),
    ("Password reset request", "Low", "Closed"),
    ("Printer not working", "Medium", "Open"),
    ("Software installation request", "Low", "Open"),
    ("Server downtime", "Critical", "Investigating"),
    ("Wi-Fi connectivity issues", "Medium", "Open"),
    ("Slow computer performance", "Low", "Resolved"),
    ("Access denied to shared folder", "High", "Open"),
    ("Email phishing alert", "High", "Investigating"),
    ("Malware detected on laptop", "Critical", "Mitigated"),
    ("Monitor flickering", "Low", "Resolved"),
    ("Phone system not working", "Medium", "Open"),
    ("Backup failure", "High", "Open"),
    ("Database connection error", "Critical", "Investigating"),
    ("VPN disconnects frequently", "Medium", "Open"),
    ("New user setup request", "Low", "Closed"),
    ("Firewall blocked legitimate traffic", "High", "Investigating"),
    ("Software license expired", "Medium", "Open")
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create it_tickets table
cur.execute("""
CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT DEFAULT 'Open',
        created_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Optional: randomize created_date within last 30 days
for ticket in sample_tickets:
    days_ago = random.randint(0, 30)
    created_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    cur.execute("""
    INSERT INTO it_tickets (title, priority, status, created_date)
    VALUES (?, ?, ?, ?)
    """, (*ticket, created_date))

conn.commit()

conn.close()