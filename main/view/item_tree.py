import tkinter as tk
from tkinter import ttk
from collections import defaultdict

class ItemTree(ttk.Treeview):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.heading("#0", text="Items")
        self.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh()

        # Subscribe to controller changes
        self.controller.set_callback(self.controller_callback)

    def controller_callback(self, key, value):
        if key == 'db_path':
            self.refresh()
        if key == 'selected_item_oid':
            # Only set selection if it's not already selected
            current = self.selection()
            if not current or current[0] != value:
                self.selection_set(value)

    def refresh(self):
        self.delete(*self.get_children())
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("SELECT OID, ParentOID, Name FROM tblItem")
        items = c.fetchall()
        conn.close()

        # Build a mapping from ParentOID to list of children
        children_map = defaultdict(list)
        item_names = {}
        for oid, parent_oid, name in items:
            children_map[parent_oid].append(oid)
            item_names[oid] = name

        def insert_items(parent_tkid, parent_oid):
            for oid in children_map.get(parent_oid, []):
                self.insert(parent_tkid, "end", iid=oid, text=item_names[oid])
                insert_items(oid, oid)

        # Start with root items (ParentOID is None)
        insert_items("", None)

    def on_select(self, event):
        selected = self.selection()
        if selected:
            if self.controller.get('selected_item_oid') != selected[0]:
                self.controller['selected_item_oid'] = selected[0]
