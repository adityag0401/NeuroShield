"""
Generate synthetic EEG-like signal data and train the epilepsy seizure detection model.
Saves the trained model as models/eeg_model.h5 for use in the app.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
import os

np.random.seed(42)
tf.random.set_seed(42)

N_FEATURES = 178
N_SAMPLES = 5000  # 2500 seizure + 2500 non-seizure

def generate_eeg_samples(n_samples=5000):
    """Generate synthetic EEG-like features (178 signal amplitude values)."""
    half = n_samples // 2

    # Non-seizure: relatively low-amplitude, stable oscillations
    non_seizure = []
    for _ in range(half):
        t = np.linspace(0, 1, N_FEATURES)
        # Alpha waves (8–13 Hz) + small noise
        signal = (
            0.2 * np.sin(2 * np.pi * 10 * t + np.random.uniform(0, 2*np.pi))
            + 0.1 * np.sin(2 * np.pi * 4 * t + np.random.uniform(0, 2*np.pi))
            + 0.05 * np.random.randn(N_FEATURES)
        )
        # Normalize to [0, 1]
        signal = (signal - signal.min()) / (signal.max() - signal.min() + 1e-8)
        non_seizure.append(signal)

    # Seizure: higher frequency, higher amplitude, more irregular (30+ Hz spikes)
    seizure = []
    for _ in range(half):
        t = np.linspace(0, 1, N_FEATURES)
        # High-frequency spikes characteristic of seizures
        signal = (
            0.5 * np.sin(2 * np.pi * 35 * t + np.random.uniform(0, 2*np.pi))
            + 0.3 * np.sin(2 * np.pi * 50 * t + np.random.uniform(0, 2*np.pi))
            + 0.2 * np.abs(np.random.randn(N_FEATURES))  # rectified noise = spikes
        )
        signal = (signal - signal.min()) / (signal.max() - signal.min() + 1e-8)
        seizure.append(signal)

    X = np.vstack([non_seizure, seizure]).astype(np.float32)
    y = np.hstack([np.zeros(half), np.ones(half)]).astype(np.float32)

    # Shuffle
    idx = np.random.permutation(n_samples)
    return X[idx], y[idx]


print("Generating synthetic EEG data...")
X, y = generate_eeg_samples(N_SAMPLES)
print(f"X shape: {X.shape}, y shape: {y.shape}, seizure ratio: {y.mean():.2f}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Building model...")
model = Sequential([
    Input(shape=(N_FEATURES,)),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

early_stop = EarlyStopping(
    monitor='val_accuracy', patience=5, restore_best_weights=True
)

print("Training...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=30,
    batch_size=64,
    callbacks=[early_stop],
    verbose=1
)

os.makedirs("models", exist_ok=True)
model.save("models/eeg_model.h5")
print(f"Model saved to models/eeg_model.h5")

loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {acc:.4f}")
