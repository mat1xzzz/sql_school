import sqlite3

from functions import (
    add_player,
    add_profile,
    add_item,
    add_to_inventory,
    get_players,
    get_items,
    get_inventory,
    add_game_session,
    get_game_sessions,
    add_experience,
    get_leaderboard,
    delete_player,
    add_achievement,
    get_achievements,
    unlock_achievement,
    get_player_achievements,
    add_quest,
    get_quests,
    assign_quest,
    get_player_quests
)

while True:
    print("\n=== SHOPPING CART DRIFT ===")
    print("1 - Add player")
    print("2 - Add profile")
    print("3 - Add item")
    print("4 - Add item to inventory")
    print("5 - Show players")
    print("6 - Show items")
    print("7 - Show inventory")
    print("8 - Add game session")
    print("9 - Show game sessions")
    print("10 - Add experience")
    print("11 - Show leaderboard")
    print("12 - Delete player")
    print("13 - Add achievement")
    print("14 - Show achievements")
    print("15 - Unlock achievement")
    print("16 - Show player achievements")
    print("17 - Add quest")
    print("18 - Show quests")
    print("19 - Assign quest")
    print("20 - Show player quests")
    print("0 - Exit")

    choice = input("Choice: ")

    try:
        if choice == "1":
            nickname = input("Nickname: ")
            email = input("Email: ")
            player_id = add_player(nickname, email)
            print("Player added, ID:", player_id)

        elif choice == "2":
            print("\nPlayers:")
            for player in get_players():
                print(player)

            player_id = int(input("Player ID: "))
            name = input("Profile name: ")
            profile_id = add_profile(player_id, name)
            print("Profile added, ID:", profile_id)

        elif choice == "3":
            name = input("Item name: ")
            item_type = input("Item type (cart / wheels / skin / boost): ")
            price = int(input("Price: "))
            rarity = input("Rarity (common / rare / epic / legendary): ")
            item_id = add_item(name, item_type, rarity, price)
            print("Item added, ID:", item_id)

        elif choice == "4":
            print("\nItems:")
            for item in get_items():
                print(item)

            profile_id = int(input("Profile ID: "))
            item_id = int(input("Item ID: "))
            quantity = int(input("Quantity: "))
            inventory_id = add_to_inventory(profile_id, item_id, quantity)
            print("Item added to inventory, ID:", inventory_id)

        elif choice == "5":
            print("\nPlayers:")
            for player in get_players():
                print(player)

        elif choice == "6":
            print("\nItems:")
            for item in get_items():
                print(item)

        elif choice == "7":
            print("\nInventory:")
            for row in get_inventory():
                print(row)

        elif choice == "8":
            print("\nPlayers:")
            for player in get_players():
                print(player)

            player_id = int(input("Player ID: "))
            login_time = input("Login time (YYYY-MM-DD HH:MM:SS): ")
            logout_time = input("Logout time (YYYY-MM-DD HH:MM:SS): ")
            score_earned = int(input("Score earned: "))
            session_id = add_game_session(player_id, login_time, logout_time, score_earned)
            print("Game session added, ID:", session_id)

        elif choice == "9":
            print("\nGame sessions:")
            for row in get_game_sessions():
                print(row)

        elif choice == "10":
            profile_id = int(input("Profile ID: "))
            amount = int(input("Experience amount: "))
            if add_experience(profile_id, amount) > 0:
                print("Experience added.")
            else:
                print("Profile with this ID was not found.")

        elif choice == "11":
            print("\nLeaderboard:")
            for row in get_leaderboard():
                print(row)

        elif choice == "12":
            print("\nPlayers:")
            for player in get_players():
                print(player)

            player_id = int(input("Enter the ID of the player to delete: "))
            if delete_player(player_id) > 0:
                print("Player deleted.")
            else:
                print("Player with this ID was not found.")

        elif choice == "13":
            title = input("Achievement title: ")
            description = input("Description: ")
            reward_points = int(input("Reward points: "))
            achievement_id = add_achievement(title, description, reward_points)
            print("Achievement added, ID:", achievement_id)

        elif choice == "14":
            print("\nAchievements:")
            for row in get_achievements():
                print(row)

        elif choice == "15":
            print("\nPlayers:")
            for player in get_players():
                print(player)

            print("\nAchievements:")
            for row in get_achievements():
                print(row)

            player_id = int(input("Player ID: "))
            achievement_id = int(input("Achievement ID: "))
            unlocked_id = unlock_achievement(player_id, achievement_id)
            print("Achievement unlocked, ID:", unlocked_id)

        elif choice == "16":
            print("\nPlayer achievements:")
            for row in get_player_achievements():
                print(row)

        elif choice == "17":
            name = input("Quest name: ")
            description = input("Description: ")
            min_level = int(input("Min level required: "))
            quest_id = add_quest(name, description, min_level)
            print("Quest added, ID:", quest_id)

        elif choice == "18":
            print("\nQuests:")
            for row in get_quests():
                print(row)

        elif choice == "19":
            print("\nQuests:")
            for row in get_quests():
                print(row)

            profile_id = int(input("Profile ID: "))
            quest_id = int(input("Quest ID: "))
            status = input("Status (in_progress / completed): ")
            progress = int(input("Progress: "))
            player_quest_id = assign_quest(profile_id, quest_id, status, progress)
            print("Quest assigned, ID:", player_quest_id)

        elif choice == "20":
            print("\nPlayer quests:")
            for row in get_player_quests():
                print(row)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

    except ValueError:
        print("Error: please enter a number where a number is required.")
    except sqlite3.Error as error:
        print("Database error:", error)