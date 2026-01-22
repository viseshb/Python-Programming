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
#  CHANGED/ADDED: need more than 2 points so internal validation split works
X = np.array([[100], [300], [600], [800], [1000], [1100]])   #  CHANGED/ADDED
y = np.array([20,    45,    95,    120,   150,    165])      #  CHANGED/ADDED

#  CHANGED/ADDED: explicit train/test split (test is truly unseen)
X_train = X[:5]   #  CHANGED/ADDED (first 5 points for training)
y_train = y[:5]   #  CHANGED/ADDED
X_test  = X[5:]   #  CHANGED/ADDED (last point for test)
y_test  = y[5:]   #  CHANGED/ADDED

# ======== Normalization ========
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  #  CHANGED/ADDED: fit ONLY on train
X_test_scaled  = scaler.transform(X_test)       #  CHANGED/ADDED

# ======== SGD Regressor with L2 Regularization + Early Stopping ========
model = SGDRegressor(
    loss='squared_error',
    penalty='l2',
    alpha=0.1,
    learning_rate='constant',
    eta0=0.01,
    random_state=42,

    #  CHANGED/ADDED: built-in early stopping on an internal validation split
    early_stopping=True,
    validation_fraction=0.2,   # 20% of TRAIN used as validation internally
    n_iter_no_change=20,       # stop if no improvement for 20 epochs
    tol=1e-4,                  # minimum improvement threshold

    #  CHANGED/ADDED: let sklearn handle epochs (max_iter = max epochs)
    max_iter=2000
)

#  CHANGED/ADDED: now just fit once (sklearn handles early stopping)
model.fit(X_train_scaled, y_train)

#  CHANGED/ADDED: how many epochs it actually ran before stopping
print(f"Epochs run (n_iter_): {model.n_iter_}")  # requires sklearn >= 0.21-ish; commonly available

final_w = model.coef_[0]
final_b = model.intercept_[0]

# ======== Prediction ========
X_example = np.array([[300]])
X_example_scaled = scaler.transform(X_example)
predicted_price = model.predict(X_example_scaled)
print(f"\nPrice of 300 sqft house: ${predicted_price[0] * 1000:.2f}")
print(f"Final w = {final_w:.4f}, Final b = {final_b:.4f}")

#  CHANGED/ADDED: final test evaluation (unseen data)
test_pred = model.predict(X_test_scaled)
test_mse = np.mean((test_pred - y_test) ** 2)
print(f"Test MSE: {test_mse:.6f}")

# ======== Save Directory ========
current_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.abspath(os.path.join(current_dir, "..", "images/Linear_regression"))
os.makedirs(save_dir, exist_ok=True)

# ======== Plot Regression Line ========
plt.scatter(X_train, y_train, label='Train Points')
plt.scatter(X_test, y_test, label='Test Point')  #  CHANGED/ADDED

x_line = np.linspace(np.min(X), np.max(X), 100).reshape(-1, 1)
x_line_scaled = scaler.transform(x_line)
y_line = model.predict(x_line_scaled)

plt.plot(x_line, y_line, label='Regression Line')
plt.xlabel("Size (sq ft)")
plt.ylabel("Price ($1000s)")
plt.title("Regularized Linear Regression (SGD + built-in Early Stopping)")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(save_dir, "Linear_regression_line_sklearn_earlystop.png"))  #  CHANGED/ADDED
plt.show()
