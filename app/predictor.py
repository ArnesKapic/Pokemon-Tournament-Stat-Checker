import os  # For checking file
import joblib  # For loading model
import pandas as pd  # For data handling
from colorama import Fore  # For themed CLI

# Loads machine learning model
def load_model(model_path):
    if not os.path.exists(model_path):
        print(f"{Fore.RED}Model not found at '{model_path}'.")
        print(f"{Fore.YELLOW}Please train and save the model first.")
        return None
    return joblib.load(model_path)

# Uses machine Learning model to predict if legendary or non-legendary
def predict(model, features):
    columns = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
    input_df = pd.DataFrame([features], columns=columns)
    prediction = model.predict(input_df)
    return prediction[0]
