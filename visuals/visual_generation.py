import pandas as pd  # For loading CSV
import matplotlib.pyplot as plt  # For creating plots
import seaborn as sns  # For stylish visuals
from sklearn.ensemble import RandomForestClassifier  # For training ML model
from sklearn.model_selection import train_test_split  # For splitting data into train/test
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay  # For evaluating predictions

# Load dataset
data_path = pd.read_csv("../data/pokemon.csv")

# 1.) Scatterplot: Attack vs Defense by Legendary status
plt.figure(figsize=(7, 4))
sns.scatterplot(
    data=data_path,
    x='attack',
    y='defense',
    hue='is_legendary',
    palette='coolwarm'
)
plt.title("Pokémon's Attack vs Defense (Legendary vs Non-Legendary)")
plt.xlabel("Attack")
plt.ylabel("Defense")
plt.legend(title="Legendary")
plt.tight_layout()
plt.savefig("visual_images/scatterplot.png")
plt.close()

# 2.) Histogram: Speed Distribution
plt.figure(figsize=(7, 4))
plt.hist(data_path['speed'].dropna(), bins=20, color='red', edgecolor='black')
plt.title("Pokémon Speed Histogram")
plt.xlabel("Speed")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("visual_images/histogram.png")
plt.close()

# 3.) Confusion Matrix: Classifier
# Clean and prepare data
stats = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
target = 'is_legendary'
clean_data_path = data_path[stats + [target]].dropna()

X = clean_data_path[stats]
Y = clean_data_path[target]

# Split into training and test sets
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train classifier
classifier_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
classifier_model.fit(train_X, train_Y)

# Generate predictions and confusion matrix
predicted_Y = classifier_model.predict(test_X)
conf_matrix = confusion_matrix(
    test_Y, predicted_Y,
    labels=[0, 1]
)

matrix_display = ConfusionMatrixDisplay(
    confusion_matrix=conf_matrix,
    display_labels=["Not Legendary", "Legendary"]
)
matrix_display.plot(cmap='Reds')
plt.title("Confusion Matrix - Legendary Classifier")
plt.tight_layout()
plt.savefig("visual_images/confusion_matrix.png")
plt.close()

print("Visualizations saved in 'visual_images/' folder!")
