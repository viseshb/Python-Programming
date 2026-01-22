import numpy as np
import os
import matplotlib.pyplot as plt 
save_dir = os.path.dirname(os.path.abspath(__file__))

# ========== Data ==========
x_train = np.array([100, 1000, 800, 1200])   # sq ft
y_train = np.array([20, 150, 120, 180])      # in $1000s

x_val   = np.array([300, 900])               # sq ft
y_val   = np.array([45, 135])                # in $1000s

x_test  = np.array([600, 1100])              # sq ft
y_test  = np.array([95, 165])                # in $1000s

# ==========================
# CHANGED/ADDED: removed Z-score normalization completely
# We will use raw x values directly.
x_train_norm = x_train   # CHANGED/ADDED (kept variable names to minimize edits)
x_val_norm   = x_val     # CHANGED/ADDED
x_test_norm  = x_test    # CHANGED/ADDED

# ========== Cost Function (NO Regularization) ==========
# CHANGED/ADDED: removed lambda_ usage and reg term
def compute_cost(x, y, w, b):
    m_local = len(x)
    total_cost = 0
    for i in range(m_local):
        f_wb_i = w * x[i] + b
        total_cost += (f_wb_i - y[i]) ** 2
    mse = total_cost / (2 * m_local)
    return mse  # CHANGED/ADDED

# ========== Gradient (NO Regularization) ==========
# CHANGED/ADDED: removed lambda_ usage and L2 gradient term
def compute_gradient(x, y, w, b):
    m_local = len(x)
    dj_dw = 0
    dj_db = 0
    for i in range(m_local):
        f_wb_i = w * x[i] + b
        dj_dw += (f_wb_i - y[i]) * x[i]
        dj_db += f_wb_i - y[i]
    dj_dw = dj_dw / m_local
    dj_db = dj_db / m_local
    return dj_dw, dj_db

# ========== Gradient Descent with Validation + Early Stopping ==========
# CHANGED/ADDED: removed lambda_ argument everywhere
def gradient_descent(x_train, y_train, x_val, y_val, w, b, alpha, num_iters,
                     patience=50, min_delta=1e-6):
    cost_history_train = []
    cost_history_val = []

    best_w, best_b = w, b
    best_val_cost = float("inf")
    patience_counter = 0

    for i in range(num_iters):
        # ---- TRAIN STEP (updates happen here) ----
        dj_dw, dj_db = compute_gradient(x_train, y_train, w, b)  # CHANGED/ADDED
        w -= alpha * dj_dw
        b -= alpha * dj_db
        train_cost = compute_cost(x_train, y_train, w, b)        # CHANGED/ADDED
        cost_history_train.append(train_cost)

        # ---- VALIDATION STEP (NO updates here) ----
        val_cost = compute_cost(x_val, y_val, w, b)              # CHANGED/ADDED
        cost_history_val.append(val_cost)

        if i % 100 == 0:
            print(
                f"Iter {i}: TrainCost={train_cost:.6f}, ValCost={val_cost:.6f}, w={w:.6f}, b={b:.6f}"
            )

        # ---- EARLY STOPPING LOGIC ----
        if val_cost < best_val_cost - min_delta:
            best_val_cost = val_cost
            best_w, best_b = w, b
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print(f"\nEarly stopping at iteration {i} (no improvement in ValCost for {patience} checks).")
            w, b = best_w, best_b
            break

    return w, b, cost_history_train, cost_history_val

# ========== Training ==========
initial_w = 0
initial_b = 0

# CHANGED/ADDED: without normalization, you usually need a much smaller alpha
alpha = 1e-7   # CHANGED/ADDED
iterations = 200  # CHANGED/ADDED (more iters since alpha is small)

final_w, final_b, train_cost_history, val_cost_history = gradient_descent(
    x_train_norm, y_train,
    x_val_norm, y_val,
    initial_w, initial_b,
    alpha, iterations,
    patience=50,   # CHANGED/ADDED (since we have many iters)
    min_delta=1e-9   # CHANGED/ADDED
)

# ========== Prediction Function ==========
# CHANGED/ADDED: removed mu/sigma since no normalization
def predict(w, x, b):
    return w * x + b  # CHANGED/ADDED

predicted_price = predict(final_w, 300, final_b)  # CHANGED/ADDED
print(f"\nPrice of 300 sqft house: ${predicted_price * 1000:.2f}")

# ========== Final TEST evaluation ==========
test_cost = compute_cost(x_test_norm, y_test, final_w, final_b)  # CHANGED/ADDED
print(f"Final Test Cost (unseen data): {test_cost:.6f}")

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..","images/Linear_regression"))
os.makedirs(save_dir, exist_ok=True)

plt.scatter(x_train, y_train, color='blue', label='Train Points')
plt.scatter(x_val, y_val, color='orange', label='Val Points')
plt.scatter(x_test, y_test, color='green', label='Test Points')

x_line = np.linspace(min(np.concatenate([x_train, x_val, x_test])),
                     max(np.concatenate([x_train, x_val, x_test])), 100)
y_line = predict(final_w, x_line, final_b)  # CHANGED/ADDED
plt.plot(x_line, y_line, color='red', label='Regression Line')
plt.xlabel("Size (sq ft)")
plt.ylabel("Price ($1000s)")
plt.title("Linear Regression")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(save_dir, "Linear_regression_line_Using_TrainValidationTest.png"))
plt.show()

# ========== Plot Cost Function ==========
plt.plot(range(len(train_cost_history)), train_cost_history, label="Train Cost")
plt.plot(range(len(val_cost_history)), val_cost_history, label="Val Cost")
plt.xlabel("Iterations")
plt.ylabel("Cost")
plt.title("Train vs Validation Cost (Early Stopping)")
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(save_dir, "Linear_Regression_train_val_cost.png"))
plt.show()
