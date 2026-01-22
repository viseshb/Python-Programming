import numpy as np
import matplotlib.pyplot as plt
import os

# ======== Load Data ========
data = np.loadtxt("C:/Users/vises/OneDrive/Desktop/Python_programming/ML/data/houses_data.csv", delimiter=",", skiprows=1)

X = data[:, :-1]  #  CHANGED (renamed to X)
y = data[:, -1]   #  CHANGED (renamed to y)

m, n = X.shape    #  CHANGED

# ======== Train/Val/Test Split ========
np.random.seed(42)  #  ADDED (reproducible)
indices = np.random.permutation(m)  #  ADDED

train_end = int(0.7 * m)  #  ADDED
val_end   = int(0.85 * m) #  ADDED

train_idx = indices[:train_end]      #  ADDED
val_idx   = indices[train_end:val_end]  #  ADDED
test_idx  = indices[val_end:]        #  ADDED

X_train, y_train = X[train_idx], y[train_idx]  #  ADDED
X_val,   y_val   = X[val_idx],   y[val_idx]    #  ADDED
X_test,  y_test  = X[test_idx],  y[test_idx]   #  ADDED

# ======== Z-score Normalization ========
def z_score_norm(x):
    mu = np.mean(x, axis=0)
    sigma = np.std(x, axis=0)
    sigma[sigma == 0] = 1
    x_norm = (x - mu) / sigma
    return x_norm, mu, sigma

#  CHANGED: normalize using TRAIN stats only
X_train_norm, x_mu, x_sigma = z_score_norm(X_train)  #  CHANGED
X_val_norm  = (X_val  - x_mu) / x_sigma              #  ADDED
X_test_norm = (X_test - x_mu) / x_sigma              #  ADDED

# ======== Cost Function with L2 Regularization ========
#  CHANGED: remove global m usage; use local m from x
def compute_cost(x, y, w, b, lambda_):
    m_local = len(x)  #  ADDED
    total_cost = 0
    for i in range(m_local):  #  CHANGED
        total_cost += (np.dot(x[i], w) + b - y[i]) ** 2
    mse = total_cost / (2 * m_local)  #  CHANGED
    reg_term = (lambda_ / (2 * m_local)) * np.sum(w ** 2)  #  CHANGED
    return mse + reg_term

# ======== Gradient Function with L2 Regularization ========
#  CHANGED: remove global m usage; use local m from x
def compute_gradient(x, y, w, b, lambda_):
    m_local = len(x)  #  ADDED
    dj_dw = np.zeros_like(w)
    dj_db = 0
    for i in range(m_local):  #  CHANGED
        error = np.dot(x[i], w) + b - y[i]
        dj_dw += error * x[i]
        dj_db += error
    dj_dw = dj_dw / m_local + (lambda_ / m_local) * w  #  CHANGED
    dj_db = dj_db / m_local  #  CHANGED
    return dj_dw, dj_db

# ======== Gradient Descent with Validation + Early Stopping ========
#  CHANGED: add x_val/y_val + early stopping
def gradient_descent(x_train, y_train, x_val, y_val, w, b, alpha, iterations, lambda_,
                     patience=50, min_delta=1e-7):
    train_cost_history = []  #  ADDED
    val_cost_history   = []  #  ADDED

    best_val_cost = float("inf")  #  ADDED
    best_w, best_b = w.copy(), b  #  ADDED
    wait = 0  #  ADDED

    for i in range(iterations):
        # ---- TRAIN STEP (updates happen ONLY here) ----
        dw, db = compute_gradient(x_train, y_train, w, b, lambda_)
        w -= alpha * dw
        b -= alpha * db

        train_cost = compute_cost(x_train, y_train, w, b, lambda_)
        val_cost   = compute_cost(x_val, y_val, w, b, lambda_)  #  ADDED (NO updates)

        train_cost_history.append(train_cost)  #  ADDED
        val_cost_history.append(val_cost)      #  ADDED

        if i % 100 == 0:
            print(f"Iteration {i}: TrainCost = {train_cost:.6f}, ValCost = {val_cost:.6f}")  #  CHANGED

        # ---- EARLY STOPPING (based on validation) ----
        #  ADDED
        if val_cost < best_val_cost - min_delta:
            best_val_cost = val_cost
            best_w, best_b = w.copy(), b
            wait = 0
        else:
            wait += 1

        if wait >= patience:
            print(f"\nEarly stopping at iteration {i} (no improvement in ValCost for {patience} checks).")
            w, b = best_w, best_b  # restore best weights
            break

    return w, b, train_cost_history, val_cost_history  #  CHANGED

# ======== Prediction Function ========
def predict(x, w, b, mu, sigma):
    x = np.array(x)
    if np.any(x < mu - 3 * sigma) or np.any(x > mu + 3 * sigma):
        print(f" Warning: Input {x.tolist()} may be out-of-distribution.")
    x_norm = (x - mu) / sigma
    return max(0, x_norm @ w + b)

# ======== Train the Model ========
initial_w = np.zeros(n)
initial_b = 0
alpha = 0.01
iterations = 5000         #  CHANGED (give room for early stopping)
lambda_ = 1

#  CHANGED: train uses TRAIN, monitors VAL
final_w, final_b, train_cost_history, val_cost_history = gradient_descent(
    X_train_norm, y_train,
    X_val_norm, y_val,
    initial_w, initial_b,
    alpha, iterations, lambda_,
    patience=200,       #  ADDED (you can tune)
    min_delta=1e-8      #  ADDED
)

#  ADDED: Evaluate test set once at the end (final unbiased check)
test_cost = compute_cost(X_test_norm, y_test, final_w, final_b, lambda_)  #  ADDED
print(f"\nFinal Test Cost (unseen data): {test_cost:.6f}")  #  ADDED

# ======== Test Predictions ========
test_houses = [
    [1000, 3, 2, 20],
    [1500, 4, 2, 5],
    [300, 2, 1, 30]
]

print("\nTest Predictions:")
for house in test_houses:
    price = predict(house, final_w, final_b, x_mu, x_sigma)
    print(f"House {house} => Predicted price: ${price * 1000:.2f}")

# ======== Final Weights Display ========
print("\nFinal Weights:")
features = ['Sqft', 'Bedrooms', 'Bathrooms', 'Age']
for i in range(n):
    print(f"{features[i]}: {final_w[i]:.4f}")
print(f"Bias: {final_b:.4f}")

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..", "images/Multiple_Linear_Regression_Using_Dataset"))
os.makedirs(save_dir, exist_ok=True)

# ======== Plot Train vs Validation Cost ========
plt.figure(figsize=(8, 5))
plt.plot(range(len(train_cost_history)), train_cost_history, label="Train Cost")  #  CHANGED
plt.plot(range(len(val_cost_history)), val_cost_history, label="Val Cost")        #  ADDED
plt.title("Train vs Validation Cost (with Early Stopping)")
plt.xlabel("Iterations")
plt.ylabel("Cost (MSE + L2 Penalty)")
plt.legend()  #  ADDED
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Multiple_linear_regression_train_val_cost.png"))  #  CHANGED
plt.show()

# ======== Feature Weight Bar Plot ========
plt.figure(figsize=(6, 4))
plt.bar(features, final_w)
plt.title("Feature Weights with Regularization")
plt.ylabel("Weight")
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Multiple_linear_regression_feature_weights_DATASET_train_val_cost.png"))
plt.show()
