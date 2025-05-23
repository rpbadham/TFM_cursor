import tkinter as tk
from tkinter import ttk
from datetime import datetime
from view.item_tree import ItemTree
from model import db

class MainWindow:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Project Delivery And Document Tracking")
        self.root.geometry("800x400")

        # Menubar
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open Database")
        filemenu.add_command(label="Create New Database")
        filemenu.add_command(label="Maintain Activity Lookup")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        # PanedWindow
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=1)

        self.left_pane = ttk.Frame(self.paned, width=320)
        self.middle_pane = ttk.Frame(self.paned, width=160)
        self.right_pane = ttk.Frame(self.paned, width=320)

        self.paned.add(self.left_pane, stretch="always")
        self.paned.add(self.middle_pane, stretch="always")
        self.paned.add(self.right_pane, stretch="always")

        # Footer
        self.footer = tk.Label(self.root, text="", anchor="w")
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_footer()

        self.item_tree = ItemTree(self.left_pane, self.controller, db)
        self.item_tree.pack(fill=tk.BOTH, expand=1)

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def update_footer(self):
        db_path = self.controller.get('db_path', '')
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.footer.config(text=f"DB: {db_path}    Date: {date_str}")

    def on_exit(self):
        self.root.destroy()
