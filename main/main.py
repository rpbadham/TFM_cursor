import os
import tkinter as tk
from view.main_window import MainWindow
from controller.controller import controller
from model import db

DEFAULT_DB_PATH = "project_tracker.db"

def ensure_db(db_path):
    new_db = not os.path.exists(db_path)
    conn = db.get_connection(db_path)
    db.create_schema(conn)
    if new_db:
        db.seed_data(conn)
    conn.close()
    return db_path

def main():
    db_path = ensure_db(DEFAULT_DB_PATH)
    controller['db_path'] = db_path

    root = tk.Tk()
    app = MainWindow(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()
