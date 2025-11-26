import numpy as np
import matplotlib.pyplot as plt
import os

# ======== Load Data ========
data = np.loadtxt("C:/Users/vises/OneDrive/Desktop/Python_programming/ML/data/houses_data.csv", delimiter=",", skiprows=1)

x_train = data[:, :-1]  # First 4 columns: features
y_train = data[:, -1]   # Last column: target
m, n = x_train.shape

# ======== Z-score Normalization ========
def z_score_norm(x):
    mu = np.mean(x, axis=0)
    sigma = np.std(x, axis=0)
    sigma[sigma == 0] = 1
    x_norm = (x - mu) / sigma
    return x_norm, mu, sigma

x_train_norm, x_mu, x_sigma = z_score_norm(x_train)

# ======== Cost Function with L2 Regularization ========
def compute_cost(x, y, w, b, lambda_):
    total_cost = 0
    for i in range(m):
        total_cost += (np.dot(x[i], w) + b - y[i]) ** 2
    mse = total_cost / (2 * m)
    reg_term = (lambda_ / (2 * m)) * np.sum(w ** 2)
    return mse + reg_term

# ======== Gradient Function with L2 Regularization ========
def compute_gradient(x, y, w, b, lambda_):
    dj_dw = np.zeros_like(w)
    dj_db = 0
    for i in range(m):
        error = np.dot(x[i], w) + b - y[i]
        dj_dw += error * x[i]
        dj_db += error
    dj_dw = dj_dw / m + (lambda_ / m) * w
    dj_db = dj_db / m
    return dj_dw, dj_db

# ======== Gradient Descent ========
def gradient_descent(x, y, w, b, alpha, iterations, lambda_):
    cost_history = []
    for i in range(iterations):
        dw, db = compute_gradient(x, y, w, b, lambda_)
        w -= alpha * dw
        b -= alpha * db
        cost = compute_cost(x, y, w, b, lambda_)
        cost_history.append(cost)
        if i % 100 == 0:
            print(f"Iteration {i}: Cost = {cost:.4f}")
    return w, b, cost_history

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
iterations = 1000
lambda_ = 1  # Regularization strength

final_w, final_b, cost_history = gradient_descent(
    x_train_norm, y_train, initial_w, initial_b, alpha, iterations, lambda_
)

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

# ======== Plot Cost Convergence ========
plt.figure(figsize=(8, 5))
plt.plot(range(iterations), cost_history)
plt.title("Cost Function Convergence with Regularization")
plt.xlabel("Iterations")
plt.ylabel("Cost (MSE + L2 Penalty)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Multiple_linear_regression_cost_convergence_DATASET.png"))
plt.show()

# ======== Feature Weight Bar Plot ========
plt.figure(figsize=(6, 4))
plt.bar(features, final_w)
plt.title("Feature Weights with Regularization")
plt.ylabel("Weight")
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Multiple_linear_regression_feature_weights_DATASET.png"))
plt.show()
