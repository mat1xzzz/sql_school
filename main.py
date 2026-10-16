import sqlite3

# Connect to DB
database = sqlite3.connect('for_game.db')
cursor = database.cursor()

# Create tables

# Players
cursor.execute("""
CREATE TABLE IF NOT EXISTS "player" (
    "id" INTEGER NOT NULL,
    "nickname" VARCHAR NOT NULL UNIQUE,
    "email" VARCHAR NOT NULL UNIQUE,
    "created_at" TIMESTAMP NOT NULL,
    PRIMARY KEY("id")
)
""")

# Player profiles (cart builds)
cursor.execute("""
CREATE TABLE IF NOT EXISTS "profile_preset" (
    "id" INTEGER NOT NULL,
    "player_id" INTEGER NOT NULL,
    "name" VARCHAR NOT NULL UNIQUE,
    "level" INTEGER NOT NULL,
    "experience" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("player_id") REFERENCES "player"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Items (carts, wheels, skins, boosts)
cursor.execute("""
CREATE TABLE IF NOT EXISTS "items" (
    "id" INTEGER NOT NULL,
    "name" VARCHAR NOT NULL UNIQUE,
    "type" VARCHAR NOT NULL,
    "rarity" VARCHAR NOT NULL,
    "value" INTEGER NOT NULL,
    PRIMARY KEY("id")
)
""")

# Player inventory
cursor.execute("""
CREATE TABLE IF NOT EXISTS "player_inventory" (
    "id" INTEGER NOT NULL,
    "profile_id" INTEGER NOT NULL,
    "item_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("profile_id") REFERENCES "profile_preset"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY ("item_id") REFERENCES "items"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Achievements
cursor.execute("""
CREATE TABLE IF NOT EXISTS "achievements" (
    "id" INTEGER NOT NULL,
    "title" VARCHAR NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "reward_points" INTEGER NOT NULL,
    PRIMARY KEY("id")
)
""")

# Unlocked achievements per player
cursor.execute("""
CREATE TABLE IF NOT EXISTS "player_achievements" (
    "id" INTEGER NOT NULL,
    "player_id" INTEGER NOT NULL,
    "achievement_id" INTEGER NOT NULL,
    "unlocked_at" TIMESTAMP NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("player_id") REFERENCES "player"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY ("achievement_id") REFERENCES "achievements"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Quests
cursor.execute("""
CREATE TABLE IF NOT EXISTS "quests" (
    "id" INTEGER NOT NULL,
    "name" VARCHAR NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "min_level_required" INTEGER NOT NULL,
    PRIMARY KEY("id")
)
""")

# Quest progress per profile
cursor.execute("""
CREATE TABLE IF NOT EXISTS "player_quests" (
    "id" INTEGER NOT NULL,
    "profile_id" INTEGER NOT NULL,
    "quest_id" INTEGER NOT NULL,
    "status" VARCHAR NOT NULL,
    "progress_count" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("profile_id") REFERENCES "profile_preset"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY ("quest_id") REFERENCES "quests"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Game sessions
cursor.execute("""
CREATE TABLE IF NOT EXISTS "game_sessions" (
    "id" INTEGER NOT NULL,
    "player_id" INTEGER NOT NULL,
    "login_time" TIMESTAMP NOT NULL,
    "logout_time" TIMESTAMP NOT NULL,
    "score_earned" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("player_id") REFERENCES "player"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Leaderboard
cursor.execute("""
CREATE TABLE IF NOT EXISTS "leaderboard" (
    "id" INTEGER NOT NULL UNIQUE,
    "player_id" INTEGER NOT NULL,
    "total_score" INTEGER NOT NULL,
    "rank_position" INTEGER NOT NULL,
    "last_updated" TIMESTAMP NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY ("player_id") REFERENCES "player"("id")
        ON UPDATE NO ACTION ON DELETE NO ACTION
)
""")

# Fill tables

# Players
cursor.execute("""
INSERT OR IGNORE INTO player (id, nickname, email, created_at)
VALUES (1, 'djrudga', 'ycfgvukhbli@mail.com', '2026-01-10 12:00:00')
""")
cursor.execute("""
INSERT OR IGNORE INTO player (id, nickname, email, created_at)
VALUES (2, 'rudapakale', 'ycxtiu@mail.com', '2026-02-15 18:30:00')
""")
cursor.execute("""
INSERT OR IGNORE INTO player (id, nickname, email, created_at)
VALUES (3, 'uhqerv', 'gyvkuh@mail.com', '2026-03-20 09:15:00')
""")

# Profiles
cursor.execute("""
INSERT OR IGNORE INTO profile_preset (id, player_id, name, level, experience)
VALUES (1, 1, 'fygiuvhbijn', 12, 3400)
""")
cursor.execute("""
INSERT OR IGNORE INTO profile_preset (id, player_id, name, level, experience)
VALUES (2, 2, 'kwemv', 8, 1800)
""")
cursor.execute("""
INSERT OR IGNORE INTO profile_preset (id, player_id, name, level, experience)
VALUES (3, 3, 'iunoin', 5, 900)
""")

# Items
cursor.execute("""
INSERT OR IGNORE INTO items (id, name, type, rarity, value)
VALUES (1, 'Rusty Cart', 'cart', 'common', 100)
""")
cursor.execute("""
INSERT OR IGNORE INTO items (id, name, type, rarity, value)
VALUES (2, 'Turbo Cart', 'wheels', 'rare', 500)
""")
cursor.execute("""
INSERT OR IGNORE INTO items (id, name, type, rarity, value)
VALUES (3, 'Neon Cart', 'skin', 'epic', 900)
""")
cursor.execute("""
INSERT OR IGNORE INTO items (id, name, type, rarity, value)
VALUES (4, 'Fire Cart', 'boost', 'common', 50)
""")

# Inventory
cursor.execute("""
INSERT OR IGNORE INTO player_inventory (id, profile_id, item_id, quantity)
VALUES (1, 1, 2, 1)
""")
cursor.execute("""
INSERT OR IGNORE INTO player_inventory (id, profile_id, item_id, quantity)
VALUES (2, 2, 3, 1)
""")
cursor.execute("""
INSERT OR IGNORE INTO player_inventory (id, profile_id, item_id, quantity)
VALUES (3, 3, 4, 5)
""")
cursor.execute("""
INSERT OR IGNORE INTO player_inventory (id, profile_id, item_id, quantity)
VALUES (4, 1, 1, 1)
""")

# Achievements
cursor.execute("""
INSERT OR IGNORE INTO achievements (id, title, description, reward_points)
VALUES (1, 'First Drift', 'Complete your first drift in the store', 50)
""")
cursor.execute("""
INSERT OR IGNORE INTO achievements (id, title, description, reward_points)
VALUES (2, 'Angle Master', 'Drift through 10 aisles without hitting a shelf', 100)
""")
cursor.execute("""
INSERT OR IGNORE INTO achievements (id, title, description, reward_points)
VALUES (3, 'Speed Demon', 'Reach top speed in the main hallway', 150)
""")

cursor.execute("""
INSERT OR IGNORE INTO player_achievements (id, player_id, achievement_id, unlocked_at)
VALUES (1, 1, 1, '2026-01-11 10:43:02')
""")
cursor.execute("""
INSERT OR IGNORE INTO player_achievements (id, player_id, achievement_id, unlocked_at)
VALUES (2, 2, 1, '2026-02-16 14:24:49')
""")
cursor.execute("""
INSERT OR IGNORE INTO player_achievements (id, player_id, achievement_id, unlocked_at)
VALUES (3, 1, 2, '2026-02-01 21:49:13')
""")

# Quests
cursor.execute("""
INSERT OR IGNORE INTO quests (id, name, description, min_level_required)
VALUES (1, 'Cereal Aisle Slide', 'Drift around the cereal aisle corner 3 times', 1)
""")
cursor.execute("""
INSERT OR IGNORE INTO quests (id, name, description, min_level_required)
VALUES (2, 'Freezer Section Chaos', 'Drift through the freezer section without crashing', 5)
""")
cursor.execute("""
INSERT OR IGNORE INTO quests (id, name, description, min_level_required)
VALUES (3, 'Midnight Mall Run', 'Beat the security guard in a full store lap', 10)
""")

cursor.execute("""
INSERT OR IGNORE INTO player_quests (id, profile_id, quest_id, status, progress_count)
VALUES (1, 1, 3, 'in_progress', 1)
""")
cursor.execute("""
INSERT OR IGNORE INTO player_quests (id, profile_id, quest_id, status, progress_count)
VALUES (2, 2, 1, 'completed', 3)
""")
cursor.execute("""
INSERT OR IGNORE INTO player_quests (id, profile_id, quest_id, status, progress_count)
VALUES (3, 3, 2, 'in_progress', 1)
""")

# Game sessions
cursor.execute("""
INSERT OR IGNORE INTO game_sessions (id, player_id, login_time, logout_time, score_earned)
VALUES (1, 1, '2026-10-15 18:28:40', '2026-10-15 18:52:38', 1200)
""")
cursor.execute("""
INSERT OR IGNORE INTO game_sessions (id, player_id, login_time, logout_time, score_earned)
VALUES (2, 2, '2026-10-15 10:32:23', '2026-10-15 11:37:54', 450)
""")
cursor.execute("""
INSERT OR IGNORE INTO game_sessions (id, player_id, login_time, logout_time, score_earned)
VALUES (3, 3, '2026-10-16 01:47:52', '2026-10-16 02:29:17', 300)
""")

# Leaderboard
cursor.execute("""
INSERT OR IGNORE INTO leaderboard (id, player_id, total_score, rank_position, last_updated)
VALUES (1, 1, 5200, 1, '2026-10-16 12:00:00')
""")
cursor.execute("""
INSERT OR IGNORE INTO leaderboard (id, player_id, total_score, rank_position, last_updated)
VALUES (2, 2, 3100, 2, '2026-10-16 12:00:00')
""")
cursor.execute("""
INSERT OR IGNORE INTO leaderboard (id, player_id, total_score, rank_position, last_updated)
VALUES (3, 3, 1500, 3, '2026-10-16 12:00:00')
""")

database.commit()

# Get data from tables

print("--- Inventory ---")
cursor.execute("""
SELECT p.nickname, pp.name, i.name, i.rarity, inv.quantity
FROM player_inventory inv
         JOIN profile_preset pp ON inv.profile_id = pp.id
         JOIN player p ON pp.player_id = p.id
         JOIN items i ON inv.item_id = i.id
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Profile: {row[1]} | Item: {row[2]} ({row[3]}) | Quantity: {row[4]}")

print("\n--- Achievements ---")
cursor.execute("""
SELECT p.nickname, a.title, a.reward_points, pa.unlocked_at
FROM player_achievements pa
         JOIN player p ON pa.player_id = p.id
         JOIN achievements a ON pa.achievement_id = a.id
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Achievement: {row[1]} | Points: {row[2]} | Unlocked: {row[3]}")

print("\n--- Quests ---")
cursor.execute("""
SELECT pp.name, q.name, pq.status, pq.progress_count
FROM player_quests pq
         JOIN profile_preset pp ON pq.profile_id = pp.id
         JOIN quests q ON pq.quest_id = q.id
""")
for row in cursor.fetchall():
    print(f"Profile: {row[0]} | Quest: {row[1]} | Status: {row[2]} | Progress: {row[3]}")

print("\n--- Game Sessions ---")
cursor.execute("""
SELECT p.nickname, gs.login_time, gs.logout_time, gs.score_earned
FROM game_sessions gs
         JOIN player p ON gs.player_id = p.id
""")
for row in cursor.fetchall():
    print(f"Player: {row[0]} | Login: {row[1]} | Logout: {row[2]} | Score: {row[3]}")

print("\n--- Leaderboard ---")
cursor.execute("""
SELECT lb.rank_position, p.nickname, lb.total_score
FROM leaderboard lb
         JOIN player p ON lb.player_id = p.id
ORDER BY lb.rank_position
""")
for row in cursor.fetchall():
    print(f"#{row[0]} | {row[1]} | Total score: {row[2]}")

database.close()