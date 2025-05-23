import sqlite3
import uuid

def get_connection(db_path):
    return sqlite3.connect(db_path)

def create_schema(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tblItem (
            OID TEXT PRIMARY KEY,
            ParentOID TEXT,
            Name TEXT,
            Description TEXT,
            Status INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tblActivityLookup (
            OID TEXT PRIMARY KEY,
            Name TEXT,
            Description TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tblActivity (
            OID TEXT PRIMARY KEY,
            ItemOID TEXT,
            ActivityLookupOID TEXT,
            Status INTEGER,
            IsOverdue INTEGER,
            Description TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tblComment (
            OID TEXT PRIMARY KEY,
            ActivityOID TEXT,
            Status INTEGER,
            Comment TEXT,
            Date TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS tblFile (
            OID TEXT PRIMARY KEY,
            ParentType TEXT,
            ParentOID TEXT,
            FileName TEXT,
            FileData BLOB
        )
    ''')
    conn.commit()

def seed_data(conn):
    c = conn.cursor()
    # Add a root item
    root_oid = str(uuid.uuid4())
    c.execute("INSERT INTO tblItem (OID, ParentOID, Name, Description, Status) VALUES (?, ?, ?, ?, ?)",
              (root_oid, None, "Sample Project", "Root project item", 1))
    # Add a child item
    child_oid = str(uuid.uuid4())
    c.execute("INSERT INTO tblItem (OID, ParentOID, Name, Description, Status) VALUES (?, ?, ?, ?, ?)",
              (child_oid, root_oid, "Subsystem A", "A subsystem", 1))
    # Add activity lookup
    lookup_oid = str(uuid.uuid4())
    c.execute("INSERT INTO tblActivityLookup (OID, Name, Description) VALUES (?, ?, ?)",
              (lookup_oid, "Inspection", "Inspection activity"))
    # Add activity
    activity_oid = str(uuid.uuid4())
    c.execute("INSERT INTO tblActivity (OID, ItemOID, ActivityLookupOID, Status, IsOverdue, Description) VALUES (?, ?, ?, ?, ?, ?)",
              (activity_oid, child_oid, lookup_oid, 1, 0, "Initial inspection"))
    # Add comment
    comment_oid = str(uuid.uuid4())
    c.execute("INSERT INTO tblComment (OID, ActivityOID, Status, Comment, Date) VALUES (?, ?, ?, ?, ?)",
              (comment_oid, activity_oid, 1, "First comment", "2024-06-01"))
    conn.commit()
