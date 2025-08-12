import numpy as np

# --- Custom Data Generator ---
def load_coffee_data():
    """ Creates a coffee roasting data set.
        roasting duration: 12-15 minutes is best
        temperature range: 175-260C is best
    """
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

# --- Sigmoid Function ---
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# --- Dense Layer (Using Matrix Multiplication!!)---
def my_dense(a_in, w, b):
    z = np.matmul(w.T, a_in) + b
    a_out = sigmoid(z)
    return a_out

# --- 2-Layer Neural Network ---
def my_sequential(x, w1, b1, w2, b2):
    a1 = my_dense(x, w1, b1)
    a2 = my_dense(a1, w2, b2)
    return a2

# --- Predict Function ---
def my_predict(X, w1, b1, w2, b2):
    m = X.shape[0]
    p = np.zeros((m, 1))
    for i in range(m):
        p[i, 0] = my_sequential(X[i], w1, b1, w2, b2).item()
    return p

# --- Main Execution --- 
X, Y = load_coffee_data()
Xn, mu, sigma = normalize(X)

# Pretrained weights from previous TensorFlow model
w1 = np.array([[-8.93, 0.29, 12.9], [-0.1, -7.32, 10.81]])
b1 = np.array([-9.82, -9.28, 0.96])
w2 = np.array([[-31.18], [-27.59], [-32.56]])
b2 = np.array([15.41])

# --- Test Predictions ---
X_test = np.array([
    [200, 13.9],  # Likely a good roast
    [200, 17.0]   # Overcooked
])
X_test_norm = (X_test - mu) / sigma
preds = my_predict(X_test_norm, w1, b1, w2, b2)

print("Raw Prediction Probabilities (Confidence Scores):")
for i in range(len(preds)):
    print(f"Example {i+1}: {preds[i, 0]:.2f}")


# Threshold for classification
yhat = (preds >= 0.5).astype(int)

print("Input Temperatures and Durations:")
print(X_test)
print("Predicted Classes (1 = Good Roast, 0 = Bad Roast):")
print(yhat)