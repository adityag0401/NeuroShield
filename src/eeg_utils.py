import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model as keras_load_model

# Path to your EEG model
MODEL_PATH = "models/eeg_model.h5"

_eeg_model_cache = None


def load_eeg_model():
    """Load the EEG seizure detection model (cached after first load)."""
    global _eeg_model_cache
    if _eeg_model_cache is None:
        _eeg_model_cache = keras_load_model(MODEL_PATH, compile=False)
    return _eeg_model_cache


def extract_signal_from_image(image: Image.Image) -> np.ndarray:
    """
    Extract a 1D EEG signal representation from an EEG graph image.

    Args:
        image: PIL Image of the EEG graph

    Returns:
        np.ndarray of shape (178,) normalized signal features
    """
    img = np.array(image.convert("L"))  # Grayscale
    edges = cv2.Canny(img, 50, 150)     # Edge detection
    signal = np.mean(edges, axis=1) / 255.0  # Normalize

    # Resize to 178 features to match training input shape
    signal_resized = cv2.resize(
        signal.reshape(-1, 1), (1, 178), interpolation=cv2.INTER_LINEAR
    ).flatten()
    return signal_resized


def predict_from_signal(signal: np.ndarray):
    """
    Predict seizure from processed EEG signal.

    Args:
        signal: np.ndarray of shape (178,)

    Returns:
        tuple: (prediction: int, confidence: float)
            prediction = 1 for SEIZURE, 0 for NON-SEIZURE
            confidence is between 0 and 1.
    """
    model = load_eeg_model()
    signal = signal.reshape(1, -1)  # Shape: (1, 178)
    raw_score = float(model.predict(signal, verbose=0)[0][0])
    prediction = int(raw_score > 0.5)
    # Confidence: distance from 0.5 mapped to 0.5..1.0
    confidence = raw_score if prediction == 1 else (1 - raw_score)
    return prediction, confidence
