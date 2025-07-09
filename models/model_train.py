import pandas as pd  # For loading CSV
from sklearn.ensemble import RandomForestClassifier  # For ML model
from sklearn.model_selection import train_test_split  # For splitting data
import joblib  # For saving trained model

# Load dataset
data_path = pd.read_csv("../data/pokemon.csv")

# Clean and prepare data
stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
target = 'is_legendary'
clean_data_path = data_path[stats + [target]].dropna()

X = clean_data_path[stats]
Y = clean_data_path[target]
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(train_X, train_Y)

# Save model
joblib.dump(model, "pokemon_model.pkl")
print("Model has been retrained and saved!")
