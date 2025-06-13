import sqlite3

conn = sqlite3.connect("file_uploads.db")
cursor = conn.cursor()

for row in cursor.execute("SELECT * FROM file_data"):
    print(row)

conn.close()
