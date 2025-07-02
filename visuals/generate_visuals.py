import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Ensure visuals directory exists
os.makedirs("visuals", exist_ok=True)

# Load dataset
df = pd.read_csv("../data/pokemon.csv")

# -------------------------------
# 1. Histogram: Speed Distribution
# -------------------------------
plt.figure(figsize=(8, 5))
plt.hist(df['speed'].dropna(), bins=20, color='skyblue', edgecolor='black')
plt.title("Pokémon Speed Distribution")
plt.xlabel("Speed")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visuals/speed_histogram.png")
plt.close()

# ---------------------------------------------
# 2. Scatterplot: Attack vs Defense by Legendary
# ---------------------------------------------
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='attack', y='defense', hue='is_legendary', palette='coolwarm')
plt.title("Attack vs Defense (Legendary vs Non-Legendary)")
plt.xlabel("Attack")
plt.ylabel("Defense")
plt.legend(title="Legendary")
plt.tight_layout()
plt.savefig("visuals/attack_vs_defense.png")
plt.close()

# --------------------------------
# 3. Confusion Matrix of Classifier
# --------------------------------
# Prepare and clean data
features = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
target = 'is_legendary'
df_clean = df[features + [target]].dropna()
X = df_clean[features]
y = df_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Not Legendary", "Legendary"])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix - Legendary Classifier")
plt.tight_layout()
plt.savefig("visuals/confusion_matrix.png")
plt.close()

print("✅ Visualizations saved in the 'visuals/' folder.")
