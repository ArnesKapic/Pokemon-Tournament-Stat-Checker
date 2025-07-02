# ===============================
# Pokémon Classifier CLI Program
# ===============================

# Standard libraries for file, system, and data handling
import joblib  # For loading the trained ML model
import pandas as pd  # For data handling
import os  # For file system checks
import sys  # For system exit and pip installation
import random  # For suggesting Pokémon
import json  # For saving and loading team data

# Optional dependency: colorized text output
try:
    from colorama import Fore, Style, init
except ImportError:
    print("Installing required package 'colorama'...")
    os.system(f"{sys.executable} -m pip install colorama")
    from colorama import Fore, Style, init

init(autoreset=True)  # Automatically reset colors after each print

# Constants for file paths and type emojis
DATA_PATH = "data/pokemon.csv"
MODEL_PATH = "models/legendary_model.pkl"
TEAM_FILE = "data/team.json"

# Mapping Pokémon types to emojis for fun, themed UI
TYPE_EMOJI = {
    "fire": "🔥", "water": "💧", "grass": "🌿", "electric": "⚡",
    "ice": "❄️", "fighting": "🥊", "poison": "☠️", "ground": "🌍",
    "flying": "🌬️", "psychic": "🔮", "bug": "🐛", "rock": "🪨",
    "ghost": "👻", "dragon": "🐉", "dark": "🌑", "steel": "⚙️",
    "fairy": "✨", "normal": "🔘", None: ""
}

# Load and clean the dataset
try:
    df = pd.read_csv(DATA_PATH)
    df_clean = df[['name', 'type1', 'type2', 'hp', 'attack', 'defense', 'sp_attack',
                   'sp_defense', 'speed']].dropna(subset=['name', 'type1'])
    stats_dict = df_clean.set_index('name').to_dict(orient='index')  # Store Pokémon data in a quick-access dict
except Exception as e:
    print(f"{Fore.RED}Error loading data: {e}")
    sys.exit(1)

# Display the app banner
def print_banner():
    banner = f"""
{Fore.YELLOW}{Style.BRIGHT}
╔═══════════════════════════════════════════════════╗
║            Legendary Pokémon Tester               ║
╠═══════════════════════════════════════════════════╣
║  Tip: You can type Pokémon names or stats.        ║
╚═══════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
    print(banner)

# Suggest random Pokémon and show type emojis
def suggest_pokemon():
    print(f"{Fore.CYAN}Here are some Pokémon you can try typing in:")
    sample = random.sample(list(stats_dict.keys()), 5)
    for name in sample:
        poke = stats_dict.get(name, {})
        type1 = poke.get("type1", "")
        type2 = poke.get("type2", "")
        emoji1 = TYPE_EMOJI.get(type1.lower(), "") if isinstance(type1, str) else ""
        emoji2 = TYPE_EMOJI.get(type2.lower(), "") if isinstance(type2, str) else ""
        types = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1 or emoji2}"
        print(f"  - {name} {types}")
    print()

# Display main menu options
def get_input_choice():
    print(f"{Fore.CYAN}\nWhat would you like to do?")
    print(f"  1. Predict single Pokémon")
    print(f"  2. Lookup by Pokémon name")
    print(f"  3. Manage Tournament Team")
    print(f"  0. Exit")
    return input("Select option: ").strip()

# Manually enter stat values
def get_stats_manually():
    try:
        hp = int(input("  HP: "))
        attack = int(input("  Attack: "))
        defense = int(input("  Defense: "))
        sp_attack = int(input("  Special Attack: "))
        sp_defense = int(input("  Special Defense: "))
        speed = int(input("  Speed: "))
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter integers only.")
        sys.exit(1)
    return [hp, attack, defense, sp_attack, sp_defense, speed]

# Retrieve stats from a Pokémon's name
def get_stats_from_name(name):
    match = stats_dict.get(name)
    if not match:
        print(f"{Fore.RED}❌ Pokémon not found. Please try a valid name.")
        return None, None, None
    print(f"{Fore.GREEN}✔ Found stats for {name}.")
    stats = [match['hp'], match['attack'], match['defense'],
             match['sp_attack'], match['sp_defense'], match['speed']]
    return stats, match.get('type1', '').lower(), match.get('type2', '').lower()

# Use ML model to predict legendary status
def predict(model, features):
    columns = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    input_df = pd.DataFrame([features], columns=columns)
    prediction = model.predict(input_df)
    return prediction[0]

# Load and save user's Pokémon team to file
def load_team():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, "r") as f:
            return json.load(f)
    return []

def save_team(team):
    with open(TEAM_FILE, "w") as f:
        json.dump(team, f, indent=2)

# Team management interface
def manage_team(model):
    team = load_team()
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
            name = input("Enter Pokémon name: ").strip()
            stats, type1, type2 = get_stats_from_name(name)
            if stats:
                team.append({"name": name, "stats": stats, "type1": type1, "type2": type2})
                save_team(team)
                print(f"{Fore.GREEN}Added {name} to your team.")

        # Adds Pokémon to team by entering stats manually
        elif choice == "2":
            name = input("Enter a nickname or placeholder name: ").strip()
            print("Enter stats:")
            stats = get_stats_manually()
            team.append({"name": name, "stats": stats})
            save_team(team)
            print(f"{Fore.GREEN}Added {name} to your team.")

        # Viewing the current team list with stats and type emojis
        elif choice == "3":
            if not team:
                print(f"{Fore.YELLOW}Your team is empty.")
            else:
                print(f"{Fore.CYAN}Current Team:")
                for i, member in enumerate(team, 1):
                    emoji1 = TYPE_EMOJI.get(member.get("type1"), "")
                    emoji2 = TYPE_EMOJI.get(member.get("type2"), "")
                    type_str = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1}{emoji2}"
                    print(f"  {i}. {member['name']} {type_str} - Stats: {member['stats']}")

        # Predicting and displaying Legendary status for each team member
        elif choice == "4":
            if not team:
                print(f"{Fore.YELLOW}No team members to classify.")
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
            confirm = input("Are you sure you want to clear your team? (y/n): ").strip().lower()
            if confirm == 'y':
                team.clear()
                save_team(team)
                print(f"{Fore.GREEN}Team cleared.")

        # Return to the main menu
        elif choice == "0":
            break
        # Handle invalid team menu input
        else:
            print(f"{Fore.RED}Invalid choice. Try again.")

# Application entry point
def main():
    print_banner()
    suggest_pokemon()

    # Load ML model
    if not os.path.exists(MODEL_PATH):
        print(f"{Fore.RED}❌ Model not found at '{MODEL_PATH}'.")
        print(f"{Fore.YELLOW}💡 Please train and save it first.")
        sys.exit(1)

    model = joblib.load(MODEL_PATH)

    # Run the main menu loop
    while True:
        choice = get_input_choice()
        # Manually enter Pokémon stats to determine if it's Legendary or not (using model prediction)
        if choice == "1":
            print(f"{Fore.CYAN}Enter stats manually:")
            stats = get_stats_manually()
            result = predict(model, stats)
            label = f"{Fore.MAGENTA}✨ Legendary!" if result == 1 else f"{Fore.GREEN}Not Legendary."
            print(f"Prediction: {label}")
        # Enter a Pokémon name to auto-fetch stats from dataset and predict Legendary status
        elif choice == "2":
            name = input("Enter Pokémon name: ").strip()
            stats, type1, type2 = get_stats_from_name(name)
            if stats:
                result = predict(model, stats)
                label = f"{Fore.MAGENTA}✨ Legendary!" if result == 1 else f"{Fore.GREEN}Not Legendary."
                emoji1 = TYPE_EMOJI.get(type1, '')
                emoji2 = TYPE_EMOJI.get(type2, '')
                type_str = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1}{emoji2}"
                print(f"{name} {type_str}: {label}")
        # Open the tournament team manager (add/view/classify/clear team)
        elif choice == "3":
            manage_team(model)
        # Exits the program
        elif choice == "0":
            print(f"{Fore.CYAN}Goodbye Trainer!")
            break
        # Handle invalid menu input
        else:
            print(f"{Fore.RED}Invalid option.")

# Starting the application
if __name__ == "__main__":
    main()
