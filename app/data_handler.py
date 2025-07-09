import pandas as pd  # For loading CSV
import sys  # Fir exiting on error
from colorama import Fore  # For themed text

# Constants for file path and weaknesses shown by emoji
DATA_PATH = "data/pokemon.csv"

# Emoji's indicated by what type the Pokémon is
TYPE_EMOJI = {
    "fire": "🔥", "water": "💧", "grass": "🌿", "electric": "⚡",
    "ice": "❄️", "fighting": "🥊", "poison": "☠️", "ground": "🌍",
    "flying": "🌬️", "psychic": "🔮", "bug": "🐛", "rock": "🪨",
    "ghost": "👻", "dragon": "🐉", "dark": "🌑", "steel": "⚙️",
    "fairy": "✨", "normal": "🔘", None: ""
}

# Loads and cleans the dataset
try:
    df = pd.read_csv(DATA_PATH)
    df_clean = df[['name', 'type1', 'type2', 'hp', 'attack', 'defense', 'sp_attack',
                   'sp_defense', 'speed']].dropna(subset=['name', 'type1'])
    stats_dict = df_clean.set_index('name').to_dict(orient='index')
except Exception as e:
    print(f"{Fore.RED}There was an error loading the data: {e}")
    sys.exit(1)
