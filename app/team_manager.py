import os  # For checking file
import json  # For saving and loading team data
from colorama import Fore, Style  # For nicely themed CLI
from app.interface import stats_manual, get_stats_from_name
from app.data_handler import TYPE_EMOJI  # For Pokémon stats and icon types
from app.predictor import predict  # For predicting legendary status

# Constant for JSON file
TEAM_FILE = "data/team.json"

# Loads Pokémon team to file
def team_load():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, "r") as f:
            return json.load(f)
    return []

# Saves Pokémon team to file
def team_save(team):
    with open(TEAM_FILE, "w") as f:
        json.dump(team, f, indent=2)

# Manages users Pokémon team
def team_manager(model):
    team = team_load()
    while True:
        print(f"""
{Fore.CYAN}{Style.BRIGHT}Team Manager:{Style.RESET_ALL}
  1. Add Pokémon by name
  2. Add Pokémon by stats
  3. View current team
  4. Classify team members
  5. Clear team
  0. Return to main menu
""")
        choice = input("Select option: ").strip()

        # Adds Pokémon to team by name (fetches stats from dataset)
        if choice == "1":
            name = input("Enter name of Pokémon: ").strip()
            stats, type1, type2 = get_stats_from_name(name)
            if stats:
                team.append({"name": name, "stats": stats, "type1": type1, "type2": type2})
                team_save(team)
                print(f"{Fore.LIGHTGREEN_EX}Added {name} to your team!")

        # Adds Pokémon to team by entering stats manually
        elif choice == "2":
            name = input("Enter a nickname: ").strip()
            print("Enter stats:")
            stats = stats_manual()
            if stats:
                team.append({"name": name, "stats": stats})
                team_save(team)
                print(f"{Fore.LIGHTGREEN_EX}Added {name} to your team!")

        # Viewing the current team list with stats and type emojis
        elif choice == "3":
            if not team:
                print(f"{Fore.LIGHTYELLOW_EX}Your team is empty.")
            else:
                print(f"{Fore.LIGHTCYAN_EX}Current Team:")
                for i, member in enumerate(team, 1):
                    emoji1 = TYPE_EMOJI.get(member.get("type1"), "")
                    emoji2 = TYPE_EMOJI.get(member.get("type2"), "")
                    type_str = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1}{emoji2}"
                    print(f"  {i}. {member['name']} {type_str} - Stats: {member['stats']}")

        # Predicting and displaying Legendary status for each team member
        elif choice == "4":
            if not team:
                print(f"{Fore.LIGHTYELLOW_EX}No team members to classify.")
            else:
                for member in team:
                    label = predict(model, member['stats'])
                    emoji1 = TYPE_EMOJI.get(member.get("type1"), "")
                    emoji2 = TYPE_EMOJI.get(member.get("type2"), "")
                    type_str = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1}{emoji2}"
                    result = "✨ Legendary" if label == 1 else "Not Legendary"
                    print(f"{member['name']} {type_str}: {result}")

        # Clearing the current team after user confirmation
        elif choice == "5":
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                team.clear()
                team_save(team)
                print(f"{Fore.LIGHTGREEN_EX}Team cleared.")
        # Return to menu
        elif choice == "0":
            break
        # Handle invalid team menu input
        else:
            print(f"{Fore.RED}Invalid choice. Try again.")
