import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import functions as f


def get_profiles():
    db = sqlite3.connect("for_game.db")
    rows = db.execute("SELECT id, player_id, name, level, experience FROM profile_preset").fetchall()
    db.close()
    return rows


# tab name: (column headers, function that returns rows)
TABLES = {
    "Players": (["ID", "Nickname", "Email", "Created"], f.get_players),
    "Profiles": (["ID", "Player ID", "Name", "Level", "XP"], get_profiles),
    "Items": (["ID", "Name", "Type", "Rarity", "Price"], f.get_items),
    "Inventory": (["ID", "Player", "Profile", "Item", "Rarity", "Qty"], f.get_inventory),
    "Leaderboard": (["Rank", "Player", "Score"], f.get_leaderboard),
}

# button text: (function, [(question, type)], returns_count)
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

root = tk.Tk()
root.title("SHOPPING CART DRIFT")

# Tabs with tables
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=8, pady=8)
trees = {}
for name, (headers, _) in TABLES.items():
    tree = ttk.Treeview(notebook, columns=headers, show="headings", height=14)
    for h in headers:
        tree.heading(h, text=h)
        tree.column(h, width=130)
    notebook.add(tree, text=name)
    trees[name] = tree


def refresh():
    for name, (_, getter) in TABLES.items():
        trees[name].delete(*trees[name].get_children())
        for row in getter():
            trees[name].insert("", "end", values=row)


def open_form(title, func, fields, returns_count):
    win = tk.Toplevel(root)
    win.title(title)
    entries = []
    for i, (question, kind) in enumerate(fields):
        tk.Label(win, text=question).grid(row=i, column=0, sticky="e", padx=6, pady=3)
        entry = tk.Entry(win, width=32)
        entry.grid(row=i, column=1, padx=6, pady=3)
        entries.append(entry)

    def submit(event=None):
        try:
            values = [int(e.get()) if kind == int else e.get()
                      for e, (_, kind) in zip(entries, fields)]
            result = func(*values)
            refresh()
        except ValueError:
            messagebox.showerror("Error", "Enter a number where a number is required.", parent=win)
            return
        except Exception as error:  # show ANY error in a window
            messagebox.showerror("Error", f"{type(error).__name__}: {error}", parent=win)
            return
        win.destroy()
        if returns_count and result == 0:
            messagebox.showwarning("Not found", "ID not found.")
        else:
            messagebox.showinfo("OK", "Done." if returns_count else f"Done, ID: {result}")

    buttons = tk.Frame(win)
    buttons.grid(row=len(fields), column=0, columnspan=2, pady=8)
    tk.Button(buttons, text="OK", width=8, command=submit).pack(side="left", padx=4)
    tk.Button(buttons, text="Cancel", width=8, command=win.destroy).pack(side="left", padx=4)
    win.bind("<Return>", submit)
    win.bind("<Escape>", lambda event: win.destroy())
    entries[0].focus_set()
    win.lift()


# Show any unexpected error in a window instead of silently in the terminal
root.report_callback_exception = lambda *err: messagebox.showerror("Error", f"{err[0].__name__}: {err[1]}")

# Buttons
bar = tk.Frame(root)
bar.pack(pady=(0, 8))
for text, (func, fields, count) in ACTIONS.items():
    tk.Button(bar, text=text,
              command=lambda t=text, a=(func, fields, count): open_form(t, *a)).pack(side="left", padx=2)

refresh()
root.mainloop()