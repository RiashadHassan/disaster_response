import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Load saved models
model_severity = tf.keras.models.load_model("fire_severity_model_transfer_learning.h5")


# Function to load and preprocess a single image
def load_and_preprocess_image(image_path):
    img = load_img(image_path, target_size=(128, 128))
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(
        img_array, axis=0
    )  # Expand dimensions to match model input shape
    return img_array


# Example image path for testing (replace with your own test image path)
cur = os.path.dirname(__file__)
test_image_path = os.path.join(cur, "test_media/non-fire-5.jpg")

# Load and preprocess the test image
test_image = load_and_preprocess_image(test_image_path)

# Predict severity score
severity_score = model_severity.predict(test_image)[0][0]
# severity_score = model_severity.predict(test_image)
print(f"Predicted Severity Score: {severity_score}")
