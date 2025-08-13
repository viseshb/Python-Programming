# Decision Boundary Plot for Coffee Roast Classifier (2-layer NN with given weights)
import numpy as np
import matplotlib.pyplot as plt
import os

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

# --- Grid for Decision Boundary ---
t_vals = np.linspace(150, 285, 300)
d_vals = np.linspace(11.5, 15.5, 300)
tt, dd = np.meshgrid(t_vals, d_vals)
grid = np.c_[tt.ravel(), dd.ravel()]
grid_norm = (grid - mu) / sigma

# Predict probabilities over the grid
grid_pred = my_predict(grid_norm, w1, b1, w2, b2).reshape(tt.shape)

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..","images/Neural_Networks"))
os.makedirs(save_dir, exist_ok=True)

# --- Plot ---
plt.figure(figsize=(8, 6))
# Filled contour for probability regions (0 to 1 with 0.5 threshold)
plt.contourf(tt, dd, grid_pred, levels=[0, 0.5, 1], cmap="bwr", alpha=0.3)
# Scatter the original points
plt.scatter(X[:, 0], X[:, 1], c=Y.flatten(), cmap="bwr", edgecolor='k', s=15)
cbar = plt.colorbar()
cbar.set_label("Probability of Good Roast")
plt.xlabel("Temperature (°C)")
plt.ylabel("Duration (min)")
plt.title("Decision Boundary: Coffee Roast Classifier")
plt.grid(True)
plt.tight_layout()

plt.savefig(os.path.join(save_dir, "Neural_Networks_Decision_Boundary_Using_Matrix_Multiplication.png"))
plt.show()
