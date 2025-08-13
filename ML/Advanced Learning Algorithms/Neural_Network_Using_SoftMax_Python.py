# Four-class softmax with NOISY data + decision regions

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Input
from keras.losses import SparseCategoricalCrossentropy
from keras.optimizers import Adam
import os

rng = np.random.default_rng(7)

def sample_X(n=300, center=(-1.5, 1.5), noise=0.25):
    cx, cy = center
    t = rng.uniform(-1.0, 1.0, size=n//2)
    line1 = np.stack([cx + t, cy + t], axis=1)
    t = rng.uniform(-1.0, 1.0, size=n - n//2)
    line2 = np.stack([cx + t, cy - t], axis=1)
    pts = np.vstack([line1, line2]) + rng.normal(0, noise, size=(n, 2))
    y = np.full(len(pts), 0)
    return pts, y

def sample_O(n=300, center=(1.5, 1.5), r=0.9, noise=0.25):
    cx, cy = center
    theta = rng.uniform(0, 2*np.pi, size=n)
    rad = r + rng.normal(0, 0.15, size=n)
    pts = np.stack([cx + rad*np.cos(theta), cy + rad*np.sin(theta)], axis=1)
    pts += rng.normal(0, noise, size=(n, 2))
    y = np.full(n, 1)
    return pts, y

def sample_square(n=300, center=(-1.5, -1.5), side=1.8, noise=0.2):
    cx, cy = center
    half = side / 2
    pts = rng.uniform([-half, -half], [half, half], size=(n, 2))
    pts += np.array([cx, cy]) + rng.normal(0, noise, size=(n, 2))
    y = np.full(n, 2)
    return pts, y

def sample_triangle(n=300, center=(1.5, -1.5), noise=0.2):
    cx, cy = center
    V = np.array([[0, 1.0], [-0.9, -0.5], [0.9, -0.5]]) + np.array([cx, cy])
    u = rng.random(n); v = rng.random(n)
    swap = u + v > 1
    u[swap] = 1 - u[swap]; v[swap] = 1 - v[swap]
    w = 1 - u - v
    pts = (u[:, None]*V[0] + v[:, None]*V[1] + w[:, None]*V[2])
    pts += rng.normal(0, noise, size=(n, 2))
    y = np.full(n, 3)
    return pts, y

# Build noisy dataset
Xx, yx = sample_X()
Xo, yo = sample_O()
Xs, ys = sample_square()
Xt, yt = sample_triangle()
X = np.vstack([Xx, Xo, Xs, Xt]).astype("float32")
y = np.concatenate([yx, yo, ys, yt]).astype("int32")

# Shuffle / split
idx = rng.permutation(len(X))
X, y = X[idx], y[idx]
split = int(0.8 * len(X))
X_train, y_train = X[:split], y[:split]
X_test,  y_test  = X[split:], y[split:]

# Model: linear logits + from_logits=True (softmax inside loss)
model = Sequential([
    Input(shape=(2,)),
    Dense(16, activation='relu'),
    Dense(16, activation='relu'),
    Dense(4, activation='linear')
])
model.compile(optimizer=Adam(1e-2),
              loss=SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=30, batch_size=64, verbose=0)
_, acc = model.evaluate(X_test, y_test, verbose=0)

# Decision regions
x_min, x_max = X[:,0].min()-0.5, X[:,0].max()+0.5
y_min, y_max = X[:,1].min()-0.5, X[:,1].max()+0.5
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 300),
                     np.linspace(y_min, y_max, 300))
grid = np.c_[xx.ravel(), yy.ravel()].astype("float32")
pred_grid = np.argmax(model.predict(grid, verbose=0), axis=1).reshape(xx.shape)

markers = {0:'x', 1:'o', 2:'s', 3:'^'}
names   = {0:'X', 1:'O', 2:'Square', 3:'Triangle'}

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..","images/Neural_Networks"))
os.makedirs(save_dir, exist_ok=True)

plt.figure(figsize=(8, 7))
plt.contourf(xx, yy, pred_grid, alpha=0.15, levels=4)
for cls in range(4):
    pts = X_train[y_train == cls]
    plt.scatter(pts[:,0], pts[:,1], marker=markers[cls], label=names[cls], s=30, alpha=0.9)

plt.legend()
plt.title(f"Four-class dataset with NOISE — Decision regions (Test Acc: {acc:.3f})")
plt.xlabel("x1"); plt.ylabel("x2")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "Neural_Networks_Decision_Boundary_Using_SoftMax.png"))
plt.show()
