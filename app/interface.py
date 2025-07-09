from colorama import Fore, Style  # For nicely themed CLI
import random  # For suggesting Pokemon
from app.data_handler import stats_dict, EMOJI_TYPE  # For Pokémon stats and icon types

# Displays the banner
def banner():
    p_banner = f"""
{Fore.LIGHTBLUE_EX}{Style.BRIGHT}
+=================================================+
|       Pokémon Stat Validation Checker           |
|               Is it Legendary?                  |
|   Tip: You can type Pokémon names or stats      |  
+=================================================+
{Style.RESET_ALL}
"""
    print(p_banner)


# Gives users some Pokémon players use while playing the game
def competitive_pokemon_preference():
    print(f"{Fore.LIGHTWHITE_EX}Some Pokémon used from competitive players:")
    sample = random.sample(list(stats_dict.keys()), 5)
    for name in sample:
        poke = stats_dict.get(name, {})
        type1 = poke.get("type1", "")
        type2 = poke.get("type2", "")
        emoji1 = EMOJI_TYPE.get(type1.lower(), "") if isinstance(type1, str) else ""
        emoji2 = EMOJI_TYPE.get(type2.lower(), "") if isinstance(type2, str) else ""
        types = f"{emoji1}/{emoji2}" if emoji1 and emoji2 else f"{emoji1 or emoji2}"
        print(f"  - {name} {types}")
    print()


# Displays the programs menu options
def user_menu():
    print(f"{Fore.LIGHTWHITE_EX}\nWhich option would you like?")
    print(f"  1. Enter Stats Manually (single Pokémon)")
    print(f"  2. Enter Name of Pokémon (single Pokémon)")
    print(f"  3. Manage Tournament Pokémon")
    print(f"  0. Close")
    return input("Select option: ").strip()


# First function allowing users to enter stats manually
def stats_manual():
    try:
        hp = int(input("  HP: "))
        attack = int(input("  Attack: "))
        defense = int(input("  Defense: "))
        sp_attack = int(input("  Special Attack: "))
        sp_defense = int(input("  Special Defense: "))
        speed = int(input("  Speed: "))
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter integers only.")
        return None
    return [hp, attack, defense, sp_attack, sp_defense, speed]


# Second function allowing users to enter Pokémon name instead of stats
def get_stats_from_name(name):
    match = stats_dict.get(name)
    if not match:
        print(f"{Fore.RED}Pokémon not found. Please try a valid name.")
        return None, None, None
    print(f"{Fore.GREEN}Found stats for {name}!")
    stats = [match['hp'], match['attack'], match['defense'],
             match['sp_attack'], match['sp_defense'], match['speed']]
    type1 = str(match.get('type1', '') or '').lower()
    type2 = str(match.get('type2', '') or '').lower()
    return stats, type1, type2
