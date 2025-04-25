import sqlite3
from config import SQLITE_DB_PATH

def extract_cdc_data():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, operation, changed_data, changed_at FROM user_changes ORDER BY id ASC")
    changes = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": c[0], "operation": c[1], "changed_data": c[2], "changed_at": c[3]} for c in changes]



# import sqlite3

# def extract_changes(db_path="sqlite.db"):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute("SELECT operation, data, timestamp FROM cdc_log")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

