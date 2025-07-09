import pandas as pd  # For loading CSV
from sklearn.ensemble import RandomForestClassifier  # For ML model
from sklearn.model_selection import train_test_split  # For splitting data
import joblib  # For saving trained model

# Load dataset
df = pd.read_csv("../data/pokemon.csv")

# Clean and prepare data
features = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
target = 'is_legendary'
df_clean = df[features + [target]].dropna()

X = df_clean[features]
y = df_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "legendary_model.pkl")
print("Model has been retrained and saved!")
