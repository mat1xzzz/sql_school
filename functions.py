import sqlite3
from datetime import datetime


def connect():
    database = sqlite3.connect("for_game.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database


# ---------------------------------- PIEVIENOT SPĒLĒTĀJU ----------------------------------
def add_player(nickname, email):
    database = connect()
    cursor = database.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO player (nickname, email, created_at) VALUES (?,?,?)",
        (nickname, email, created_at)
    )
    database.commit()
    player_id = cursor.lastrowid
    database.close()
    return player_id



# ---------------------------------- PIEVIENOT PROFILU ----------------------------------
def add_profile(player_id, name):
    database = connect()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO profile_preset (player_id, name, level, experience) VALUES (?,?,1,0)",
        (player_id, name)
    )
    database.commit()
    profile_id = cursor.lastrowid
    database.close()
    return profile_id



# ---------------------------------- PIEVIENOS PRIEKŠMETU ----------------------------------
def add_item(name, item_type, rarity, value):
    database = connect()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO items (name, type, rarity, value) VALUES (?,?,?,?)",
        (name, item_type, rarity, value)
    )
    database.commit()
    item_id = cursor.lastrowid
    database.close()
    return item_id



# ---------------------------------- PIEVIENOT INVENTĀRU ----------------------------------
def add_to_inventory(profile_id, item_id, quantity):
    database = connect()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO player_inventory (profile_id, item_id, quantity) VALUES (?,?,?)",
        (profile_id, item_id, quantity)
    )
    database.commit()
    inventory_id = cursor.lastrowid
    database.close()
    return inventory_id


# ---------------------------------- IZSAUKT SPĒLĒTĀJA SARAKSTU ----------------------------------
def get_players():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT id, nickname, email, created_at FROM player")
    players = cursor.fetchall()
    database.close()
    return players



# ---------------------------------- IZSAUKT PIEKŠMETU SARAKSTU ----------------------------------
def get_items():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT id, name, type, rarity, value FROM items")
    items = cursor.fetchall()
    database.close()
    return items



# ---------------------------------- IZSAUKT INVENTĀRU ----------------------------------
def get_inventory():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
                   SELECT inv.id,
                          player.nickname,
                          profile_preset.name,
                          items.name,
                          items.rarity,
                          inv.quantity
                   FROM player_inventory inv
                            JOIN profile_preset
                                 ON inv.profile_id = profile_preset.id
                            JOIN player
                                 ON profile_preset.player_id = player.id
                            JOIN items
                                 ON inv.item_id = items.id
                   ORDER BY inv.id
                   """)
    inventory = cursor.fetchall()
    database.close()
    return inventory



# ---------------------------------- PIEVIENOT SESSIJU ----------------------------------
def add_game_session(player_id, login_time, logout_time, score_earned):
    database = connect()
    cursor = database.cursor()
    cursor.execute(
        "INSERT INTO game_sessions (player_id, login_time, logout_time, score_earned) VALUES (?,?,?,?)",
        (player_id, login_time, logout_time, score_earned)
    )
    database.commit()
    session_id = cursor.lastrowid
    database.close()
    return session_id



# ---------------------------------- PIEVIENOT EXPERIENCE ----------------------------------
def add_experience(profile_id, amount):
    # Adds experience to a profile and recalculates its level
    # (every 1000 XP = +1 level, level 1 starts at 0 XP)
    database = connect()
    cursor = database.cursor()
    cursor.execute(
        "UPDATE profile_preset SET experience = experience + ? WHERE id = ?",
        (amount, profile_id)
    )
    cursor.execute(
        "UPDATE profile_preset SET level = experience / 1000 + 1 WHERE id = ?",
        (profile_id,)
    )
    database.commit()
    updated = cursor.rowcount
    database.close()
    return updated



# ---------------------------------- IZSAUKT TOPU ----------------------------------
def get_leaderboard():
    # Returns the leaderboard sorted by rank (best player first)
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
                   SELECT leaderboard.rank_position,
                          player.nickname,
                          leaderboard.total_score
                   FROM leaderboard
                            JOIN player
                                 ON leaderboard.player_id = player.id
                   ORDER BY leaderboard.rank_position
                   """)
    leaderboard = cursor.fetchall()
    database.close()
    return leaderboard



# ! ! ! ----------------------------------   IZDZĒST SPELĒTĀJU (AR CLAUDE PALĪDZĪBU)   ---------------------------------- ! ! !
def delete_player(player_id):
    database = connect()
    cursor = database.cursor()
    # Foreign keys are ON, so child rows must be deleted first
    cursor.execute("""DELETE FROM player_inventory
                      WHERE profile_id IN (SELECT id FROM profile_preset WHERE player_id = ?)""", (player_id,))
    cursor.execute("""DELETE FROM player_quests
                      WHERE profile_id IN (SELECT id FROM profile_preset WHERE player_id = ?)""", (player_id,))
    cursor.execute("DELETE FROM profile_preset WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM player_achievements WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM game_sessions WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM leaderboard WHERE player_id = ?", (player_id,))
    cursor.execute("DELETE FROM player WHERE id = ?", (player_id,))
    database.commit()
    deleted = cursor.rowcount  # 1 if the player existed, 0 if not
    database.close()
    return deleted
