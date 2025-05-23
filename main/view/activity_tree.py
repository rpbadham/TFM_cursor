import tkinter as tk
from tkinter import ttk

class ActivityTree(ttk.Treeview):
    def __init__(self, parent, controller, db):
        super().__init__(parent, columns=("status", "desc"))
        self.controller = controller
        self.db = db
        self.heading("#0", text="Activity")
        self.heading("status", text="Status")
        self.heading("desc", text="Description")
        self.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh()

        self.controller.set_callback(self.controller_callback)

    def controller_callback(self, key, value):
        if key in ('selected_item_oid', 'selected_activity_lookupOid'):
            self.refresh()

    def refresh(self):
        self.delete(*self.get_children())
        item_oid = self.controller.get('selected_item_oid', '')
        lookup_oids = self.controller.get('selected_activity_lookupOid', [])
        if not item_oid or not lookup_oids:
            return
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        for lookup_oid in lookup_oids:
            c.execute("""
                SELECT OID, Status, Description 
                FROM tblActivity 
                WHERE ItemOID=? AND ActivityLookupOID=?
            """, (item_oid, lookup_oid))
            for oid, status, desc in c.fetchall():
                self.insert("", "end", iid=oid, text=oid, values=(status, desc))
        conn.close()

    def on_select(self, event):
        selected = self.selection()
        if selected:
            self.controller['selected_activity_oid'] = selected[0]
