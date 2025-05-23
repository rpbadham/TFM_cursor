import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ActivityLookupPopup(tk.Toplevel):
    def __init__(self, parent, db, controller):
        super().__init__(parent)
        self.db = db
        self.controller = controller
        self.title("Maintain Activity Lookup")
        self.geometry("400x300")
        self.resizable(False, False)

        self.tree = ttk.Treeview(self, columns=("Name", "Description"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="Add", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("SELECT OID, Name, Description FROM tblActivityLookup")
        for oid, name, desc in c.fetchall():
            self.tree.insert("", "end", iid=oid, values=(name, desc))
        conn.close()

    def add_entry(self):
        name = simpledialog.askstring("Add Activity Type", "Name:", parent=self)
        if not name:
            return
        desc = simpledialog.askstring("Add Activity Type", "Description:", parent=self)
        if desc is None:
            desc = ""
        import uuid
        oid = str(uuid.uuid4())
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("INSERT INTO tblActivityLookup (OID, Name, Description) VALUES (?, ?, ?)", (oid, name, desc))
        conn.commit()
        conn.close()
        self.refresh()

    def edit_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Edit", "Select an entry to edit.")
            return
        oid = selected[0]
        old_name, old_desc = self.tree.item(oid, "values")
        name = simpledialog.askstring("Edit Activity Type", "Name:", initialvalue=old_name, parent=self)
        if not name:
            return
        desc = simpledialog.askstring("Edit Activity Type", "Description:", initialvalue=old_desc, parent=self)
        if desc is None:
            desc = ""
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("UPDATE tblActivityLookup SET Name=?, Description=? WHERE OID=?", (name, desc, oid))
        conn.commit()
        conn.close()
        self.refresh()

    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select an entry to delete.")
            return
        oid = selected[0]
        if not messagebox.askyesno("Delete", "Are you sure you want to delete this activity type?"):
            return
        conn = self.db.get_connection(self.controller['db_path'])
        c = conn.cursor()
        c.execute("DELETE FROM tblActivityLookup WHERE OID=?", (oid,))
        conn.commit()
        conn.close()
        self.refresh() 