import pandas as pd  # For loading CSV
import sys  # Fir exiting on error
from colorama import Fore  # For themed text

# Constants for file path and weaknesses shown by emoji
POKEMON_DATA_FILE = "data/pokemon.csv"

# Emoji's indicated by what type the Pokémon is
EMOJI_TYPE = {
    "fire": "🔥", "water": "💧", "grass": "🍃", "electric": "⚡",
    "ice": "❄️", "fighting": "🥊", "poison": "💀", "ground": "🌍",
    "flying": "🪽", "psychic": "🔮", "bug": "🐛", "rock": "🪨",
    "ghost": "👻", "dragon": "🐲", "dark": "🌑", "steel": "🔩",
    "fairy": "✨", "normal": "🔘", None: ""
}

# Loads and cleans the dataset
try:
    data_path = pd.read_csv(POKEMON_DATA_FILE)
    clean_data_path = data_path[['name', 'type1', 'type2', 'hp', 'attack', 'defense', 'sp_attack',
                                 'sp_defense', 'speed']].dropna(subset=['name', 'type1'])
    stats_dict = clean_data_path.set_index('name').to_dict(orient='index')
except Exception as e:
    print(f"{Fore.RED}Invalid. Data not loaded: {e}")
    sys.exit(1)
