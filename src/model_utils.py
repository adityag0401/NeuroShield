# src/model_utils.py

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Full human-readable label mapping
label_map = {
    'Mild Impairment': 'Mild',
    'Moderate Impairment': 'Moderate',
    'No Impairment': 'No Impairment',
    'Very Mild Impairment': 'Very Mild',
}

# Short-code to full display label
display_labels = {
    'Mild': 'Mild Impairment',
    'Moderate': 'Moderate Impairment',
    'No': 'No Impairment',
    'VeryMild': 'Very Mild Impairment',
    'No Impairment': 'No Impairment',
    'Very Mild': 'Very Mild Impairment',
}

labels = list(label_map.values())


def load_model():
    """Load the Alzheimer's MRI classification model."""
    return tf.keras.models.load_model("models/best_model.keras", compile=False)


def predict_image(model, img_path):
    """
    Predict the Alzheimer's stage from an MRI image.

    Returns:
        tuple: (label: str, confidence: float) where confidence is between 0 and 1.
    """
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))
    label = labels[predicted_class]

    # Map short code back to full human-readable display label
    full_label = display_labels.get(label, label)
    return full_label, confidence
