import tkinter as tk
from tkinter import ttk

class CommentTree(ttk.Treeview):
    def __init__(self, parent, controller, db):
        super().__init__(parent, columns=("status", "comment", "date"))
        self.controller = controller
        self.db = db
        self.heading("#0", text="Comment")
        self.heading("status", text="Status")
        self.heading("comment", text="Comment")
        self.heading("date", text="Date")
        self.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh()

        self.controller.set_callback(self.controller_callback)

    def controller_callback(self, key, value):
        if key == 'selected_activity_oid':
            self.refresh()

    def refresh(self):
        self.delete(*self.get_children())
        activity_oid = self.controller.get('selected_activity_oid', '')
        if not activity_oid:
            return
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("""
            SELECT OID, Status, Comment, Date 
            FROM tblComment 
            WHERE ActivityOID=?
        """, (activity_oid,))
        for oid, status, comment, date in c.fetchall():
            self.insert("", "end", iid=oid, text=oid, values=(status, comment, date))
        conn.close()

    def on_select(self, event):
        selected = self.selection()
        if selected:
            self.controller['selected_comment_oid'] = selected[0]
