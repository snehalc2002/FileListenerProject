import os
import time
import sqlite3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_FOLDER = "watched_files"

def setup_database():
    conn = sqlite3.connect("file_uploads.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        data TEXT
    )
    """)
    conn.commit()
    conn.close()

def upload_to_db(file_path):
    try:
        filename = os.path.basename(file_path)
        with open(file_path, 'r') as file:
            content = file.read()
        
        conn = sqlite3.connect("file_uploads.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO file_data (filename, data) VALUES (?, ?)", (filename, content))
        conn.commit()
        conn.close()
        print(f"Uploaded: {filename}")
    except Exception as e:
        print(f"Error: {e}")

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"New file detected: {event.src_path}")
            upload_to_db(event.src_path)

def start_listener():
    if not os.path.exists(WATCHED_FOLDER):
        os.makedirs(WATCHED_FOLDER)

    setup_database()

    print(f"Watching folder: {WATCHED_FOLDER}")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_listener()
