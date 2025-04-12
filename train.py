import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

# Sample dataset (Replace with real survey data)
X_train = np.array([
    [5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [3, 3, 3, 3, 3], [4, 5, 1, 2, 3],
    [2, 1, 5, 4, 3], [5, 5, 4, 4, 3], [1, 2, 1, 2, 1], [4, 4, 4, 4, 4]
])
y_train = ["Extrovert", "Introvert", "Balanced", "Analytical", "Creative", "Leader", "Shy", "Adventurer"]

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("personality_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as personality_model.pkl")
