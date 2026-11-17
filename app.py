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
# Theme & Color Palette Constants (Modern Grey + Colorful Accents)
# ---------------------------------------------------------
BG_COLOR = "#313338"       # Modern neutral grey (Background)
SURFACE_COLOR = "#3b3f45"  # Lighter grey (Cards, tables, notebook)
PRIMARY_COLOR = "#3b82f6"  # Vivid blue for primary actions
PRIMARY_HOVER = "#60a5fa"  # Lighter blue for hover
TEXT_COLOR = "#f4f4f5"     # Near-white for clear readability
MUTED_TEXT = "#9ca3af"     # Medium grey for secondary text
BORDER_COLOR = "#4b5058"   # Subtle border grey
INPUT_BG = "#202225"       # Dark input field background

# Colorful accent per action button: text -> (style key, base color, hover color)
ACCENTS = {
    "Add player":       ("blue",   "#3b82f6", "#2563eb"),
    "Add profile":      ("purple", "#8b5cf6", "#7c3aed"),
    "Add item":         ("amber",  "#f59e0b", "#d97706"),
    "Add to inventory": ("green",  "#10b981", "#059669"),
    "Add game session": ("cyan",   "#06b6d4", "#0891b2"),
    "Add experience":   ("orange", "#f97316", "#ea580c"),
    "Delete player":    ("red",    "#ef4444", "#dc2626"),
}

root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use('clam')

style.configure(".", background=BG_COLOR, foreground=TEXT_COLOR, font=("Segoe UI", 10))
style.configure("TFrame", background=BG_COLOR)
style.configure("Header.TLabel", font=("Georgia", 26, "bold italic"), foreground=TEXT_COLOR, background=BG_COLOR,
                anchor="center")
style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground=MUTED_TEXT, background=BG_COLOR,
                anchor="center")

# Standard Button Styling (neutral grey, modern flat look)
style.configure("TButton",
                background="#4b5058",
                foreground=TEXT_COLOR,
                borderwidth=0,
                focusthickness=0,
                padding=(14, 9),
                font=("Segoe UI", 9, "bold"))
style.map("TButton",
          background=[('active', '#5a606a'), ('pressed', '#202225')],
          foreground=[('disabled', MUTED_TEXT)])

# Colorful Accent Button Styling — one vivid color per action
for _text, (_key, _base, _hover) in ACCENTS.items():
    _style_name = f"Accent.{_key}.TButton"
    style.configure(_style_name,
                    background=_base,
                    foreground="#ffffff",
                    borderwidth=0,
                    focusthickness=0,
                    padding=(8, 8),
                    font=("Segoe UI", 10, "bold"))
    style.map(_style_name,
              background=[('active', _hover), ('pressed', '#202225')],
              foreground=[('active', '#ffffff'), ('pressed', '#ffffff'), ('disabled', '#ffffff')])

# Primary Accent Button Styling (blue — used for modal Submit)
style.configure("Primary.TButton",
                background=PRIMARY_COLOR,
                foreground="#ffffff",
                borderwidth=0,
                focusthickness=0,
                padding=(14, 9),
                font=("Segoe UI", 9, "bold"))
style.map("Primary.TButton",
          background=[('active', PRIMARY_HOVER), ('pressed', '#202225')],
          foreground=[('active', '#ffffff')])

# Notebook & Tabs Styling (modern flat tabs with blue selection)
style.configure("TNotebook", background=BG_COLOR, borderwidth=0, tabmargins=(0, 0, 0, 8))
style.configure("TNotebook.Tab",
                background=SURFACE_COLOR,
                foreground=MUTED_TEXT,
                padding=[18, 10],
                borderwidth=0,
                font=("Segoe UI", 10, "bold"))
style.map("TNotebook.Tab",
          background=[('selected', PRIMARY_COLOR), ('active', '#4b5058')],
          foreground=[('selected', '#ffffff'), ('active', TEXT_COLOR)])

# Treeview / Tables Styling
style.configure("Treeview",
                background=SURFACE_COLOR,
                foreground=TEXT_COLOR,
                fieldbackground=SURFACE_COLOR,
                borderwidth=0,
                relief="flat",
                rowheight=32,
                font=("Segoe UI", 10))
style.map("Treeview",
          background=[('selected', PRIMARY_COLOR)],
          foreground=[('selected', '#ffffff')])
style.configure("Treeview.Heading",
                background="#202225",
                foreground=TEXT_COLOR,
                borderwidth=0,
                relief="flat",
                padding=(8, 8),
                font=("Segoe UI", 10, "bold"))
style.map("Treeview.Heading", background=[('active', '#2f3237')])

# Scrollbar Styling (thin, blends with surface)
style.configure("Vertical.TScrollbar",
                background="#4b5058",
                troughcolor=BG_COLOR,
                borderwidth=0,
                arrowsize=12)
style.map("Vertical.TScrollbar", background=[('active', '#5a606a')])

# Entry Field Styling (dark fields with subtle borders)
style.configure("TEntry",
                fieldbackground=INPUT_BG,
                foreground=TEXT_COLOR,
                borderwidth=1,
                insertcolor=TEXT_COLOR,
                padding=(6, 6))
style.map("TEntry",
          bordercolor=[('focus', PRIMARY_COLOR), ('!focus', BORDER_COLOR)])

# Combobox Styling (table selector dropdown)
root.option_add("*TCombobox*Listbox.background", SURFACE_COLOR)
root.option_add("*TCombobox*Listbox.foreground", TEXT_COLOR)
root.option_add("*TCombobox*Listbox.selectBackground", PRIMARY_COLOR)
root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
style.configure("TCombobox",
                fieldbackground=INPUT_BG,
                background="#4b5058",
                foreground=TEXT_COLOR,
                borderwidth=1,
                arrowcolor=TEXT_COLOR,
                padding=(8, 6))
style.map("TCombobox",
          bordercolor=[('focus', PRIMARY_COLOR), ('!focus', BORDER_COLOR)],
          fieldbackground=[('readonly', INPUT_BG)],
          foreground=[('readonly', TEXT_COLOR)])

# ---------------------------------------------------------
# Main UI Layout
# ---------------------------------------------------------
main_frame = ttk.Frame(root, padding=24)
main_frame.pack(fill="both", expand=True)

# App Title Header (centered logo + subtitle)
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 16))
ttk.Label(header_frame, text="S H O P P I N G   C A R T   D R I F T",
          style="Header.TLabel").pack(fill="x")
ttk.Label(header_frame, text="SQL Database on SQLite  ·  Shopping Cart Drift Game Manager",
          style="Subtitle.TLabel").pack(fill="x", pady=(4, 0))

# ---------------------------------------------------------
# Action Toolbar (created & packed BEFORE the table view so it
# always keeps its space when the window is resized —
# the table shrinks instead of hiding the buttons)
# ---------------------------------------------------------
bar = ttk.Frame(main_frame)
bar.pack(side="bottom", fill="x", pady=(12, 0))

action_buttons = []
for text, (func, fields, count) in ACTIONS.items():
    style_key, _, _ = ACCENTS[text]
    btn = ttk.Button(bar, text=text, style=f"Accent.{style_key}.TButton",
                     command=lambda t=text, a=(func, fields, count): open_form(t, *a))
    action_buttons.append(btn)

BTN_GAP = 4  # matches padx between buttons


def relayout_buttons(event=None):
    """Flows the action buttons onto multiple rows when the window is too narrow."""
    width = bar.winfo_width()
    if width < 50:
        return
    rows, current, x = [], [], 0
    for btn in action_buttons:
        w = btn.winfo_reqwidth()
        need = w if not current else w + BTN_GAP
        if current and x + need > width:
            rows.append(current)
            current, x = [btn], w
        else:
            current.append(btn)
            x += need
    if current:
        rows.append(current)
    for r, row in enumerate(rows):
        for c, btn in enumerate(row):
            btn.grid(row=r, column=c, padx=(0, BTN_GAP), pady=4, sticky="ew")
    for col in range(max(len(r) for r in rows)):
        bar.columnconfigure(col, weight=1)


bar.bind("<Configure>", relayout_buttons)

# ---------------------------------------------------------
# Table Selector (single dropdown) & Table View
# ---------------------------------------------------------
table_bar = ttk.Frame(main_frame)
table_bar.pack(fill="x", pady=(0, 12))

table_var = tk.StringVar(value=list(TABLES.keys())[0])
table_selector = ttk.Combobox(table_bar, textvariable=table_var,
                              values=list(TABLES.keys()),
                              state="readonly", width=26,
                              font=("Segoe UI", 11, "bold"))
table_selector.pack(side="left", ipady=2)

table_container = ttk.Frame(main_frame)
table_container.pack(fill="both", expand=True, pady=(0, 16))

tree_scroll = ttk.Scrollbar(table_container)
tree_scroll.pack(side="right", fill="y")

# Уменьшили height с 16 до 10, чтобы таблица не занимала слишком много места по вертикали
tree = ttk.Treeview(table_container, show="headings", yscrollcommand=tree_scroll.set, height=14)
tree_scroll.config(command=tree.yview)
tree.pack(fill="both", expand=True)


def set_table_columns():
    """Applies the column headers of the currently selected table."""
    headers = TABLES[table_var.get()][0]
    tree["columns"] = headers
    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=150, anchor="w")


def on_table_selected(event=None):
    set_table_columns()
    refresh()


table_selector.bind("<<ComboboxSelected>>", on_table_selected)
set_table_columns()


def refresh():
    """Refreshes the current table view from its backend database getter."""
    getter = TABLES[table_var.get()][1]
    tree.delete(*tree.get_children())
    for row in getter():
        tree.insert("", "end", values=row)


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