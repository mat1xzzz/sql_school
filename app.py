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
    "Show game sessions": (["ID", "Login time", "Logout time", "Score earned"], f.get_game_sessions),
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
    "Add experience": (f.add_experience, [("Profile ID", int), ("Amount", int)], True),
    "Delete player": (f.delete_player, [("Player ID", int)], True),
}

# Initialize main window (увеличили высоту до 720, чтобы всё гарантированно помещалось)
root = tk.Tk()
root.title("SHOPPING CART DRIFT")
root.geometry("1024x720")
root.minsize(840, 560)

# ---------------------------------------------------------
# Theme & Color Palette Constants (Monochrome Dark Grey)
# ---------------------------------------------------------
BG_COLOR = "#404040"       # Darkest grey (Background)
SURFACE_COLOR = "#5E5D5D"  # Slightly lighter grey (Cards, tables, notebook)
PRIMARY_COLOR = "#52525b"  # Mid-grey for primary actions/buttons
PRIMARY_HOVER = "#71717a"  # Lighter mid-grey for button hover
TEXT_COLOR = "#f4f4f5"     # Near-white for clear readability
MUTED_TEXT = "#a1a1aa"     # Medium grey for secondary text
BORDER_COLOR = "#3f3f46"   # Subtle border grey

root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('clam')

style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TFrame", background=BG_COLOR)
style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground=TEXT_COLOR, background=BG_COLOR)

# Standard Button Styling
style.configure("TButton",
                background="#27272a",
                foreground=TEXT_COLOR,
                borderwidth=1,
                focusthickness=2,
                focuscolor=PRIMARY_HOVER,
                padding=(12, 8),
                font=("Segoe UI", 9, "bold"))
style.map("TButton",
          background=[('active', '#3f3f46'), ('pressed', '#18181b')],
          bordercolor=[('active', BORDER_COLOR)])

# Primary Accent Button Styling
style.configure("Primary.TButton",
                background=PRIMARY_COLOR,
                foreground="#ffffff",
                borderwidth=0,
                padding=(12, 8),
                font=("Segoe UI", 9, "bold"))
style.map("Primary.TButton",
          background=[('active', PRIMARY_HOVER), ('pressed', '#3f3f46')],
          foreground=[('active', '#ffffff')])

# Notebook & Tabs Styling
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab",
                background="#18181b",
                foreground=MUTED_TEXT,
                padding=[16, 10],
                font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab",
          background=[('selected', SURFACE_COLOR), ('active', '#27272a')],
          foreground=[('selected', TEXT_COLOR), ('active', TEXT_COLOR)])

# Treeview / Tables Styling
style.configure("Treeview",
                background=SURFACE_COLOR,
                foreground=TEXT_COLOR,
                fieldbackground=SURFACE_COLOR,
                borderwidth=0,
                rowheight=32,
                font=("Segoe UI", 10))
style.configure("Treeview.Heading",
                background="#27272a",
                foreground=TEXT_COLOR,
                font=("Segoe UI", 10, "bold"),
                relief="flat")
style.map("Treeview.Heading", background=[('active', '#3f3f46')])

# ---------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------
main_frame = ttk.Frame(root, padding=24)
main_frame.pack(fill="both", expand=True)

# App Title Header
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 16))
ttk.Label(header_frame, text="Shopping Cart Drift", style="Header.TLabel").pack(side="left")

# Notebook Container with Tables & Scrollbars
notebook_container = ttk.Frame(main_frame)
notebook_container.pack(fill="both", expand=True, pady=(0, 16))

notebook = ttk.Notebook(notebook_container)
notebook.pack(fill="both", expand=True)

trees = {}
for name, (headers, _) in TABLES.items():
    tab_frame = ttk.Frame(notebook, padding=12)
    notebook.add(tab_frame, text=name)

    tree_scroll = ttk.Scrollbar(tab_frame)
    tree_scroll.pack(side="right", fill="y")

    # Уменьшили height с 16 до 10, чтобы таблица не занимала слишком много места по вертикали
    tree = ttk.Treeview(tab_frame, columns=headers, show="headings", yscrollcommand=tree_scroll.set, height=10)
    tree_scroll.config(command=tree.yview)

    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=150, anchor="w")

    tree.pack(fill="both", expand=True)
    trees[name] = tree

# Action Toolbar (Under the tables)
bar = ttk.Frame(main_frame)
bar.pack(fill="x")

for text, (func, fields, count) in ACTIONS.items():
    is_primary = "Add" in text
    btn_style = "Primary.TButton" if is_primary else "TButton"

    btn = ttk.Button(bar, text=text, style=btn_style,
                     command=lambda t=text, a=(func, fields, count): open_form(t, *a))
    btn.pack(side="left", padx=(0, 8), pady=4)


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


root.report_callback_exception = lambda *err: messagebox.showerror("Error", f"{err[0].__name__}: {err[1]}")

refresh()

root.mainloop()