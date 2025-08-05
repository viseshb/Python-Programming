import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.exceptions import ConvergenceWarning

# ======== Suppress Convergence Warnings ========
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# ======== Data ========
x_train = np.array([[100], [1000]])  # 2D shape required
y_train = np.array([20, 150])

# ======== Normalization ========
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)

# ======== SGD Regressor with L2 Regularization ========
model = SGDRegressor(loss='squared_error', penalty='l2', alpha=0.1, learning_rate='constant', eta0=0.01,
                     max_iter=1, warm_start=True, random_state=42)

iterations = 1000
cost_history = []

for i in range(iterations):
    model.fit(x_train_scaled, y_train)
    y_pred = model.predict(x_train_scaled)
    cost = np.mean((y_pred - y_train) ** 2) / 2 + (0.1 / 2) * np.sum(model.coef_ ** 2)
    cost_history.append(cost)

    if i % 100 == 0:
        print(f"Iteration {i}: Cost = {cost:.4f}, w = {model.coef_[0]:.4f}, b = {model.intercept_[0]:.4f}")

final_w = model.coef_[0]
final_b = model.intercept_[0]

# ======== Prediction ========
x_test = np.array([[300]])
x_test_scaled = scaler.transform(x_test)
predicted_price = model.predict(x_test_scaled)
print(f"\nPrice of 300 sqft house: ${predicted_price[0] * 1000:.2f}")
print(f"Final w = {final_w:.4f}, Final b = {final_b:.4f}")

# ======== Save Directory ========
current_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.abspath(os.path.join(current_dir, "..", "images/Linear_regression"))
os.makedirs(save_dir, exist_ok=True)

# ======== Plot Regression Line ========
plt.scatter(x_train, y_train, color='blue', label='Data Points')
x_line = np.linspace(100, 1000, 100).reshape(-1, 1)
x_line_scaled = scaler.transform(x_line)
y_line = model.predict(x_line_scaled)
plt.plot(x_line, y_line, color='red', label='Regression Line')
plt.xlabel("Size (sq ft)")
plt.ylabel("Price ($1000s)")
plt.title("Regularized Linear Regression (SGD with L2)")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(save_dir, "Linear_regression_line_sklearn.png"))
plt.show()

# ======== Plot Cost Function Convergence ========
plt.plot(range(iterations), cost_history)
plt.xlabel("Iterations")
plt.ylabel("Cost")
plt.title("Cost Function Convergence (L2 Regularization)")
plt.grid(True)
plt.savefig(os.path.join(save_dir, "Linear_Regression_cost_convergence_sklearn.png"))
plt.show()
