# For interface involving banner, Pokémon suggestions, menu, input helper
from app.interface import banner, competitive_pokemon_preference, user_menu, stats_manual, get_stats_from_name

# For ML model involving loading the predictions
from app.predictor import load_model, predict

# For team creation and management functions
from app.team_manager import team_manager
import sys  # For closing the program
from colorama import Fore  # For themed CLI

# Constant for ML model
MODEL_PATH = "models/legendary_model.pkl"

# Application Core
def main():
    banner()
    competitive_pokemon_preference()

    model = load_model(MODEL_PATH)
    if model is None:
        sys.exit(1)

    while True:
        choice = user_menu()

        # Manually enter Pokémon stats to determine if it's Legendary or not (using model prediction)
        if choice == "1":
            print(f"{Fore.CYAN}Enter stats manually:")
            stats = stats_manual()
            result = predict(model, stats)
            label = f"{Fore.RED}\u2728 Legendary!" if result == 1 else f"{Fore.GREEN}Not Legendary."
            print(f"Prediction: {label}")

        # Entering a Pokémon name to auto-fetch stats from dataset and predict Legendary status
        elif choice == "2":
            name = input("Enter Pokémon name: ").strip()
            stats, type1, type2 = get_stats_from_name(name)
            if stats:
                result = predict(model, stats)
                emoji1 = ""
                emoji2 = ""
                from app.data_handler import TYPE_EMOJI  # optional lazy import
                if type1: emoji1 = TYPE_EMOJI.get(type1, '')
                if type2: emoji2 = TYPE_EMOJI.get(type2, '')
                type_str = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1}{emoji2}"
                label = f"{Fore.MAGENTA}\u2728 Legendary!" if result == 1 else f"{Fore.GREEN}Not Legendary."
                print(f"{name} {type_str}: {label}")

        # Open the tournament team manager (add/view/classify/clear team)
        elif choice == "3":
            team_manager(model)

        # Closing the program
        elif choice == "0":
            print(f"{Fore.CYAN}Goodbye Trainer!")
            break
        # Handle invalid menu input
        else:
            print(f"{Fore.RED}Invalid option.")

# Starting the application
if __name__ == "__main__":
    main()
