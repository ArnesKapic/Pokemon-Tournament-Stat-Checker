import pandas as pd  # For loading CSV
import matplotlib.pyplot as plt  # For creating plots
import seaborn as sns  # For stylish visuals
from sklearn.ensemble import RandomForestClassifier  # For training ML model
from sklearn.model_selection import train_test_split  # For splitting data into train/test
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay  # For evaluating predictions

# Load dataset
df = pd.read_csv("../data/pokemon.csv")

# 1.) Scatterplot: Attack vs Defense by Legendary
plt.figure(figsize=(7, 4))
sns.scatterplot(data=df, x='attack', y='defense', hue='is_legendary', palette='coolwarm')
plt.title("Attack vs Defense (Legendary vs Non-Legendary)")
plt.xlabel("Attack")
plt.ylabel("Defense")
plt.legend(title="Legendary")
plt.tight_layout()
plt.savefig("visual_images/scatterplot.png")
plt.close()

# 2.) Histogram: Speed Distribution
plt.figure(figsize=(7, 4))
plt.hist(df['speed'].dropna(), bins=20, color='red', edgecolor='black')
plt.title("Pokémon Speed Histogram")
plt.xlabel("Speed")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visual_images/histogram.png")
plt.close()

# 3.) Confusion Matrix: Classifier
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
disp.plot(cmap='Reds')
plt.title("CM Legendary Classifier")
plt.tight_layout()
plt.savefig("visual_images/confusion_matrix.png")
plt.close()

print("Visualizations saved in 'visuals/' folder!")
