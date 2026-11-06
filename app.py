import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import functions as f


def get_profiles():
    db = sqlite3.connect("for_game.db")
    rows = db.execute("SELECT id, player_id, name, level, experience FROM profile_preset").fetchall()
    db.close()
    return rows


# Tab configuration: (column headers, getter function)
TABLES = {
    "Players": (["ID", "Nickname", "Email", "Created"], f.get_players),
    "Profiles": (["ID", "Player ID", "Name", "Level", "XP"], get_profiles),
    "Items": (["ID", "Name", "Type", "Rarity", "Price"], f.get_items),
    "Inventory": (["ID", "Player", "Profile", "Item", "Rarity", "Qty"], f.get_inventory),
    "Leaderboard": (["Rank", "Player", "Score"], f.get_leaderboard),
}

# Action button configuration: (function, [(field_label, type)], returns_count)
ACTIONS = {
    "Add player": (f.add_player, [("Nickname", str), ("Email", str)], False),
    "Add profile": (f.add_profile, [("Player ID", int), ("Profile name", str)], False),
    "Add item": (f.add_item, [("Name", str), ("Type (cart/wheels/skin/boost)", str),
                              ("Rarity (common/rare/epic/legendary)", str), ("Price", int)], False),
    "Add to inventory": (f.add_to_inventory, [("Profile ID", int), ("Item ID", int), ("Quantity", int)], False),
    "Add game session": (f.add_game_session, [("Player ID", int), ("Login (YYYY-MM-DD HH:MM:SS)", str),
                                              ("Logout (YYYY-MM-DD HH:MM:SS)", str), ("Score", int)], False),
    "Show game sessions": (f.get_game_sessions, [("Player ID", int)], False),
    "Add experience": (f.add_experience, [("Profile ID", int), ("Amount", int)], True),
    "Delete player": (f.delete_player, [("Player ID", int)], True),
}

# Initialize main window
root = tk.Tk()
root.title("SHOPPING CART DRIFT")
root.geometry("1024x640")
root.minsize(840, 520)

# ---------------------------------------------------------
# Theme & Color Palette Constants
# ---------------------------------------------------------
BG_COLOR = "#f8fafc"  # Slate 50 (Soft neutral background)
SURFACE_COLOR = "#ffffff"  # White
PRIMARY_COLOR = "#4f46e5"  # Indigo 600
PRIMARY_HOVER = "#4338ca"  # Indigo 700
TEXT_COLOR = "#0f172a"  # Slate 900
MUTED_TEXT = "#64748b"  # Slate 500
BORDER_COLOR = "#cbd5e1"  # Slate 300

root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('clam')

style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TFrame", background=BG_COLOR)
style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=TEXT_COLOR, background=BG_COLOR)

# Standard Button Styling (Clean, flat rectangular look)
style.configure("TButton",
                background="#ffffff",
                foreground=TEXT_COLOR,
                borderwidth=1,
                focusthickness=2,
                focuscolor=PRIMARY_COLOR,
                padding=(12, 8),
                font=("Segoe UI", 9, "bold"))
style.map("TButton",
          background=[('active', '#f1f5f9'), ('pressed', '#e2e8f0')],
          bordercolor=[('active', BORDER_COLOR)])

# Primary Accent Button Styling (Indigo background for primary actions)
style.configure("Primary.TButton",
                background=PRIMARY_COLOR,
                foreground="#ffffff",
                borderwidth=0,
                padding=(12, 8),
                font=("Segoe UI", 9, "bold"))
style.map("Primary.TButton",
          background=[('active', PRIMARY_HOVER), ('pressed', '#3730a3')],
          foreground=[('active', '#ffffff')])

# Notebook & Tabs Styling
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab",
                background="#e2e8f0",
                foreground=MUTED_TEXT,
                padding=[16, 10],
                font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab",
          background=[('selected', SURFACE_COLOR), ('active', '#cbd5e1')],
          foreground=[('selected', PRIMARY_COLOR), ('active', TEXT_COLOR)])

# Treeview / Tables Styling
style.configure("Treeview",
                background=SURFACE_COLOR,
                foreground=TEXT_COLOR,
                fieldbackground=SURFACE_COLOR,
                borderwidth=0,
                rowheight=34,
                font=("Segoe UI", 10))
style.configure("Treeview.Heading",
                background="#f1f5f9",
                foreground=TEXT_COLOR,
                font=("Segoe UI", 10, "bold"),
                relief="flat")
style.map("Treeview.Heading", background=[('active', '#e2e8f0')])

# ---------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------
main_frame = ttk.Frame(root, padding=24)
main_frame.pack(fill="both", expand=True)

# App Title Header
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 16))
ttk.Label(header_frame, text="Shopping Cart Drift", style="Header.TLabel").pack(side="left")

# Action Toolbar
bar = ttk.Frame(main_frame)
bar.pack(fill="x", pady=(0, 16))

for text, (func, fields, count) in ACTIONS.items():
    # Highlight 'Add' actions as primary buttons
    is_primary = "Add" in text
    btn_style = "Primary.TButton" if is_primary else "TButton"

    btn = ttk.Button(bar, text=text, style=btn_style,
                     command=lambda t=text, a=(func, fields, count): open_form(t, *a))
    btn.pack(side="left", padx=(0, 8), pady=4)

# Notebook Container with Tables & Scrollbars
notebook_container = ttk.Frame(main_frame)
notebook_container.pack(fill="both", expand=True)

notebook = ttk.Notebook(notebook_container)
notebook.pack(fill="both", expand=True)

trees = {}
for name, (headers, _) in TABLES.items():
    tab_frame = ttk.Frame(notebook, padding=12)
    notebook.add(tab_frame, text=name)

    tree_scroll = ttk.Scrollbar(tab_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(tab_frame, columns=headers, show="headings", yscrollcommand=tree_scroll.set, height=16)
    tree_scroll.config(command=tree.yview)

    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=150, anchor="w")

    tree.pack(fill="both", expand=True)
    trees[name] = tree


def refresh():
    """Refreshes all table views from backend database getters."""
    for name, (_, getter) in TABLES.items():
        trees[name].delete(*trees[name].get_children())
        for row in getter():
            trees[name].insert("", "end", values=row)


def open_form(title, func, fields, returns_count):
    """Opens a clean, centered modal dialog window for user actions/inputs."""
    win = tk.Toplevel(root)
    win.title(title)
    win.geometry("440x380")
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()
    win.configure(bg=BG_COLOR)

    form_frame = ttk.Frame(win, padding=24)
    form_frame.pack(fill="both", expand=True)

    ttk.Label(form_frame, text=title, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w",
                                                                          pady=(0, 16))

    entries = []
    for i, (question, kind) in enumerate(fields, start=1):
        ttk.Label(form_frame, text=question).grid(row=i, column=0, sticky="w", pady=6)
        entry = ttk.Entry(form_frame, width=28)
        entry.grid(row=i, column=1, sticky="ew", pady=6, padx=(12, 0))
        entries.append(entry)

    form_frame.columnconfigure(1, weight=1)

    def submit(event=None):
        try:
            values = [int(e.get()) if kind == int else e.get()
                      for e, (_, kind) in zip(entries, fields)]
            result = func(*values)
            refresh()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number where required.", parent=win)
            return
        except Exception as error:
            messagebox.showerror("Error", f"{type(error).__name__}: {error}", parent=win)
            return

        win.destroy()
        if returns_count and result == 0:
            messagebox.showwarning("Not found", "The specified ID was not found.", parent=root)
        else:
            if isinstance(result, list):
                messagebox.showinfo("Result", f"Retrieved {len(result)} record(s). Check database or table view.",
                                    parent=root)
            else:
                messagebox.showinfo("Success",
                                    "Done." if returns_count else f"Successfully completed. Result/ID: {result}",
                                    parent=root)

    # Action Buttons Inside Modal
    btn_frame = ttk.Frame(form_frame)
    btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="e", pady=(24, 0))

    ttk.Button(btn_frame, text="Cancel", command=win.destroy).pack(side="right", padx=(8, 0))
    ttk.Button(btn_frame, text="Submit", style="Primary.TButton", command=submit).pack(side="right")

    win.bind("<Return>", submit)
    win.bind("<Escape>", lambda event: win.destroy())

    if entries:
        entries[0].focus_set()

    # Center modal relative to main window
    win.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (win.winfo_width() // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (win.winfo_height() // 2)
    win.geometry(f"+{x}+{y}")
    win.lift()


# Show any unexpected error in a clean window dialog
root.report_callback_exception = lambda *err: messagebox.showerror("Error", f"{err[0].__name__}: {err[1]}")

# Initial data load
refresh()

# Start application main loop
root.mainloop()