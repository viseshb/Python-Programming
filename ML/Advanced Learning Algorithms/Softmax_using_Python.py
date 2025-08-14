import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.datasets import mnist
import matplotlib.pyplot as plt
import random
import os

# ======== Visualization Directory ========
current_dir = os.path.dirname(__file__)
save_dir = os.path.abspath(os.path.join(current_dir, "..","images/Neural_Networks"))
os.makedirs(save_dir, exist_ok=True)

# ------------------------
# Softmax (stable)
# ------------------------
def my_softmax(z):
    z_shifted = z - np.max(z)
    exp_z = np.exp(z_shifted)
    return exp_z / np.sum(exp_z)

# Quick check
z = np.array([1., 2., 3., 4.])
print("my_softmax(z):        ", my_softmax(z))
print("tf.nn.softmax(z):     ", tf.nn.softmax(z).numpy())

# ------------------------
# Load & preprocess MNIST
# ------------------------
(X_train, y_train), (X_test, y_test) = mnist.load_data()
print("Original shapes:", X_train.shape, y_train.shape, X_test.shape, y_test.shape)

X_train = (X_train.astype("float32") / 255.0).reshape(len(X_train), -1)  # (60000, 784)
X_test  = (X_test.astype("float32")  / 255.0).reshape(len(X_test), -1)   # (10000, 784)
print("After flattening:", X_train.shape, X_test.shape)

# ------------------------
# Build model
# ------------------------
tf.random.set_seed(1234)
n = X_train.shape[1]
model = Sequential([
    Dense(25, activation='relu', input_shape=(n,), name='L1'),
    Dense(15, activation='relu', name='L2'),
    Dense(10, activation='linear', name='L3')  # logits for 10 classes
], name="my_model")

model.summary()

# ------------------------
# Compile & train
# ------------------------
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics=['accuracy']
)

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=0
)

# ------------------------
# Plots: Loss & Accuracy
# ------------------------
plt.figure()
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Test Loss')
plt.legend()
plt.title('Loss over Epochs')
plt.xlabel('Epoch'); plt.ylabel('Loss')
plt.savefig(os.path.join(save_dir, "Loss over Epochs.png"))
plt.show()

plt.figure()
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Test Acc')
plt.legend()
plt.title('Accuracy over Epochs')
plt.xlabel('Epoch'); plt.ylabel('Accuracy')
plt.savefig(os.path.join(save_dir, "Accuracy over Epochs.png"))
plt.show()

# ------------------------
# Single prediction example
# ------------------------
sample = X_test[0].reshape(1, -1)
logits = model.predict(sample, verbose=0)
probs = tf.nn.softmax(logits).numpy()
print("Raw logits:", logits)
print("Probabilities:", probs)
print("Predicted class:", np.argmax(probs))
print("True label:", y_test[0])

# ------------------------
# Grid of predictions (5x5)
# ------------------------
num_images = 25
indices = random.sample(range(len(X_test)), num_images)

plt.figure(figsize=(10, 10))
for i, idx in enumerate(indices):
    img = X_test[idx].reshape(28, 28)
    true_label = y_test[idx]
    logits_i = model.predict(X_test[idx].reshape(1, -1), verbose=0)
    pred_label = int(np.argmax(tf.nn.softmax(logits_i).numpy()))

    plt.subplot(5, 5, i + 1)
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    color = 'green' if pred_label == true_label else 'red'
    plt.title(f"T:{true_label} P:{pred_label}", color=color, fontsize=10)

plt.suptitle("MNIST Predictions (Green = Correct, Red = Wrong)", fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "NIST Predictions.png"))
plt.show()

# ------------------------
# Confusion matrix (no sklearn)
# ------------------------
y_pred_logits = model.predict(X_test, verbose=0)
y_pred = np.argmax(y_pred_logits, axis=1)
cm = tf.math.confusion_matrix(labels=y_test, predictions=y_pred, num_classes=10).numpy()

print("\nConfusion Matrix (rows=True label, cols=Pred):\n")
# Pretty-print small matrix
for r in cm:
    print(" ".join(f"{int(x):5d}" for x in r))

