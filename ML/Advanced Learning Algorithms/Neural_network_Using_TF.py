import numpy as np
import tensorflow as tf

# --- Custom Data Generator ---
def load_coffee_data():
    rng = np.random.default_rng(2)
    X = rng.random(400).reshape(-1, 2)
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

# --- Main Execution ---
X, Y = load_coffee_data()
Xn, mu, sigma = normalize(X)

# --- TensorFlow Model Definition ---
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(2,)),          # 2 input features
    tf.keras.layers.Dense(3, activation='sigmoid'),  # Hidden layer with 3 neurons
    tf.keras.layers.Dense(1, activation='sigmoid')   # Output layer (binary classification)
])

# --- Set Pretrained Weights ---
# Layer 1: weights shape (2, 3), biases shape (3,)
w1 = np.array([[-8.93, 0.29, 12.9], [-0.1, -7.32, 10.81]])
b1 = np.array([-9.82, -9.28, 0.96])

# Layer 2: weights shape (3, 1), biases shape (1,)
w2 = np.array([[-31.18], [-27.59], [-32.56]])
b2 = np.array([15.41])

# Set weights manually
model.set_weights([w1, b1, w2, b2])

# --- Test Predictions ---
X_test = np.array([
    [200, 13.9],  # Likely good roast
    [200, 17.0]   # Overcooked
])
X_test_norm = (X_test - mu) / sigma

# Predict
preds = model.predict(X_test_norm)

# Output
print("Raw Prediction Probabilities (Confidence Scores):")
for i in range(len(preds)):
    print(f"Example {i+1}: {preds[i, 0]:.2f}")

yhat = (preds >= 0.5).astype(int)

print("Input Temperatures and Durations:")
print(X_test)
print("Predicted Classes (1 = Good Roast, 0 = Bad Roast):")
print(yhat)
