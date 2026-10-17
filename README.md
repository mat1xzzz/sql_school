# Shopping Cart Drift
This is a program with a window where you can see and change the database of a game about drifting with shopping carts.

## Files

- `create_db.py` - makes the database and adds some test data (run it one time)
- `functions.py` - all functions for the database
- `app.py` - the program with the window (run this one)
- `for_game.db` - the database (it appears after you run the first file)

All files must be in the same folder.

## What you need

- Python 3.14
- Tk 

## How to install (Windows)
 
1. Go to https://www.python.org/downloads/ and download the Python installer for Windows.
2. Open the installer. **Important:** at the first screen turn on the checkbox **"Add python.exe to PATH"**, then click Install Now. Tk is already inside.
3. Open the project folder in File Explorer, click on the address bar, type `cmd` and press Enter. A black window (Command Prompt) opens in the right folder.
4. Make a virtual environment and turn it on:
```
python -m venv .venv
.venv\Scripts\activate
```
 
 
If you use PowerShell and it says that running scripts is disabled, use Command Prompt (cmd) instead, or run this first:
 
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
 
### Check that Tk works:
```
python -m tkinter
```

## How to install (for Mac/Linux)

You need Python with Tk. There are two ways how to install it.

### Way 1 - without Homebrew (easier)

1. Go to https://www.python.org/downloads/ and download the Python installer for macOS.
2. Open the file and click Continue until it is installed. Tk is already inside, you don't need anything more.
3. Open Terminal, go to the project folder and make a virtual environment:

```
cd /Users/jegors.vonogs/IT/school_sql
python3 -m venv .venv
source .venv/bin/activate
```



### Way 2 - with Homebrew

If you don't have Homebrew, install it first from https://brew.sh. Or choose Way 1.

Then:

```
brew install python-tk@3.14
cd /Users/jegors.vonogs/IT/school_sql
/opt/homebrew/bin/python3.14 -m venv .venv
source .venv/bin/activate
```

### Check that Tk works (both ways)

```
python -m tkinter
```

A small window should open. If it opens, everything is ok.

## How to start

First, make the database (only one time):

```
python create_db.py
```

Then start the program:

```
python app.py
```

Next time you only need these 3 lines:

```
cd /Users/jegors.vonogs/IT/school_sql
source .venv/bin/activate
python app.py
```

## How it works

At the top there are tabs: Players, Profiles, Items, Inventory, Leaderboard. Click a tab to see the table.

At the bottom there are buttons. Click a button, fill in the fields and press OK. Press Cancel (or Esc) if you changed your mind. The tables update by themselves.

## Buttons

| Button | What to write |
|--------|---------------|
| Add player | nickname, email (both must be new) |
| Add profile | player ID, profile name |
| Add item | name, type (cart / wheels / skin / boost), rarity (common / rare / epic / legendary), price |
| Add to inventory | profile ID, item ID, quantity |
| Add game session | player ID, login time, logout time, score |
| Add experience | profile ID, amount |
| Delete player | player ID |

Time must look like this: `2026-10-17 18:00:00`

IDs are in the first column of the tables, so look there first.

Every 1000 XP gives +1 level.

Be careful with Delete player. It deletes the player and everything about him (profiles, inventory, sessions...). You can't undo it.

<h1 align="center">
Thanks and GL!
</h1>
