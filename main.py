import sqlite3

database = sqlite3.connect('for_game.db')  # Izveidot tabulas
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS "player" (
    "id" INTEGER NOT NULL,
    "nickname" VARCHAR NOT NULL UNIQUE,
    "email" VARCHAR NOT NULL UNIQUE,
    "created_at" TIMESTAMP NOT NULL,
    PRIMARY KEY("id")
)
""")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS "achievements" (
    "id" INTEGER NOT NULL,
    "title" VARCHAR NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "reward_points" INTEGER NOT NULL,
    PRIMARY KEY("id")
)
""")

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS "quests" (
    "id" INTEGER NOT NULL,
    "name" VARCHAR NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    "min_level_required" INTEGER NOT NULL,
    PRIMARY KEY("id")
)
""")

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

database.commit()
database.close()