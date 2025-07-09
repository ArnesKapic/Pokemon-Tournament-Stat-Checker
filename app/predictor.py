import os  # For checking file
import joblib  # For loading model
import pandas as pd  # For data handling
from colorama import Fore  # For themed CLI

# Loads ML model
def model_load(model_filepath):
    if not os.path.exists(model_filepath):
        print(f"{Fore.RED}Model not found. Train/Save the model?")
        return None

    model = joblib.load(model_filepath)
    print(f"{Fore.LIGHTGREEN_EX}The model loaded successfully!")
    return model

# Classifies if Pokémon is legendary or not using ML model
def model_predict(model, features):
    stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    input_data_path = pd.DataFrame([features], columns=stats)
    prediction = model.predict(input_data_path)
    return prediction[0]
