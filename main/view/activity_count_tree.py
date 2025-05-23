import tkinter as tk
from tkinter import ttk

class ActivityCountTree(ttk.Treeview):
    def __init__(self, parent, controller, db):
        super().__init__(parent, columns=("count",))
        self.controller = controller
        self.db = db
        self.heading("#0", text="Activity Type")
        self.heading("count", text="Count")
        self.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh()

        self.controller.set_callback(self.controller_callback)

    def controller_callback(self, key, value):
        if key == 'selected_item_oid':
            self.refresh()

    def refresh(self):
        self.delete(*self.get_children())
        item_oid = self.controller.get('selected_item_oid', '')
        if not item_oid:
            return
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("""
            SELECT ActivityLookupOID, COUNT(*) 
            FROM tblActivity 
            WHERE ItemOID=? 
            GROUP BY ActivityLookupOID
        """, (item_oid,))
        for lookup_oid, count in c.fetchall():
            self.insert("", "end", iid=lookup_oid, text=lookup_oid, values=(count,))
        conn.close()

    def on_select(self, event):
        selected = self.selection()
        if selected:
            self.controller['selected_activity_lookupOid'] = [selected[0]]
