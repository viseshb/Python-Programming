import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.losses import BinaryCrossentropy
from keras.models import Sequential
import matplotlib.pyplot as plt
import os

# --- Custom Data Generator ---
def load_coffee_data():
    rng = np.random.default_rng(2)
    X = rng.random(2000).reshape(-1, 2)
    X[:, 1] = X[:, 1] * 4 + 11.5          # Duration: 11.5 - 15.5
    X[:, 0] = X[:, 0] * (285 - 150) + 150 # Temperature: 150 - 285

    Y = np.zeros(len(X))
    for i, (t, d) in enumerate(X):
        y = -3 / (260 - 175) * t + 21
        if (175 < t < 260 and 12 < d < 15 and d <= y):
            Y[i] = 1
    return X, Y.reshape(-1, 1)

# --- Feature Normalization ---
def normalize(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    return (X - mu) / sigma, mu, sigma

# --- Load and Normalize Data ---
X, Y = load_coffee_data()
Xn, mu, sigma = normalize(X)

# --- Model Definition ---
model = Sequential([    
    Dense(10, activation='relu'),       # First hidden layer: 10 neurons, ReLU activation for non-linearity
    Dense(5, activation='relu'),        # Second hidden layer: 5 neurons, ReLU activation
    Dense(1, activation='sigmoid')      # Output layer: 1 neuron, sigmoid to output probability between 0 and 1
    # Dense(1, activation='linear')     # (Alternative) Output raw logits instead of probabilities
])

model.compile(loss=BinaryCrossentropy())        # Binary cross-entropy loss; expects probabilities (from_logits=False by default)
# model.compile(loss=BinaryCrossentropy(from_logits=True))  # Use this if output layer is linear (logits); loss will apply sigmoid internally


# --- Train Model ---
model.fit(Xn, Y, epochs=300)

# --- Evaluate Accuracy on Training Set ---
train_preds = (model.predict(Xn) >= 0.5).astype(int)
train_acc = np.mean(train_preds == Y)
print(f"\n✅ Training Accuracy: {train_acc * 100:.2f}%")

# --- Test Predictions ---
X_test = np.array([
    [200, 13.9],  # Likely good roast
    [200, 17.0],  # Overcooked
    [250, 12.8],  # Edge case
    [180, 12.0],  # Near lower bounds
    [170, 14.0],  # Too cool
    [260, 15.0]   # At upper bound
])
X_test_norm = (X_test - mu) / sigma
preds = model.predict(X_test_norm)
yhat = (preds >= 0.5).astype(int)

# --- Display Predictions ---
print("\n📊 Raw Prediction Probabilities (Confidence Scores):")
for i in range(len(preds)):
    print(f"Example {i+1}: {preds[i, 0]:.2f}")

print("\n🧾 Input Temperatures and Durations:")
print(X_test)
print("🧠 Predicted Classes (1 = Good Roast, 0 = Bad Roast):")
print(yhat)

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..","images/Neural_Networks"))
os.makedirs(save_dir, exist_ok=True)

# --- Decision Boundary Plot ---
t_vals = np.linspace(150, 285, 100)
d_vals = np.linspace(11.5, 15.5, 100)
tt, dd = np.meshgrid(t_vals, d_vals)
grid = np.c_[tt.ravel(), dd.ravel()]
grid_norm = (grid - mu) / sigma
grid_pred = model.predict(grid_norm).reshape(tt.shape)

plt.figure(figsize=(8, 6))
plt.contourf(tt, dd, grid_pred, levels=[0, 0.5, 1], cmap="bwr", alpha=0.3)
plt.scatter(X[:, 0], X[:, 1], c=Y.flatten(), cmap="bwr", edgecolor='k', s=15)
plt.colorbar(label="Probability of Good Roast")
plt.xlabel("Temperature (°C)")
plt.ylabel("Duration (min)")
plt.title("Decision Boundary: Coffee Roast Classifier")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Neural_Networks_Decision_Boundary_Using_TF.png"))
plt.show()
