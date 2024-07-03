import os
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
)
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam

# Paths to directories
image_dir = r"C:\Users\WALTON\Downloads\Large-Fire\all_images"
labels_csv = r"C:\Users\WALTON\Downloads\Large-Fire\updated_labels.csv"

# Load labels CSV
labels_df = pd.read_csv(labels_csv)

# Add a column with the full path to the images
labels_df["file_path"] = labels_df.apply(
    lambda row: os.path.join(image_dir, row["filename"]), axis=1
)


# Function to load and preprocess images
def load_and_preprocess_image(file_path):
    img = load_img(file_path, target_size=(128, 128))  # Using 128x128 for VGG16
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    return img_array


# Load images and labels
X = np.zeros((len(labels_df), 128, 128, 3))
y = labels_df[
    "severity"
].values  # Use severity as the label, with 0 indicating non-fire

for idx, row in labels_df.iterrows():
    file_path = row["file_path"]
    X[idx] = load_and_preprocess_image(file_path)

# Manually split data into training and validation sets (80% training, 20% validation)
split_idx = int(0.8 * len(X))
X_train, X_val = X[:split_idx], X[split_idx:]
y_train, y_val = y[:split_idx], y[split_idx:]

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode="nearest",
)

# Load the VGG16 model pre-trained on ImageNet
base_model = VGG16(weights="imagenet", include_top=False, input_shape=(128, 128, 3))

# Freeze the convolutional base
for layer in base_model.layers:
    layer.trainable = False

# Add new layers for fine-tuning
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)  # Added dropout for regularization
predictions = Dense(1, activation="linear")(x)  # Output layer for severity regression

# Define the model
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(
    optimizer=Adam(learning_rate=0.001), loss="mean_squared_error", metrics=["mae"]
)

model.summary()

# Train the model
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    epochs=50,
    validation_data=(X_val, y_val),
)

# Save the model
model.save("fire_severity_model_transfer_learning.h5")

# Evaluate the model
loss, mae = model.evaluate(X_val, y_val)
print(f"Model - Mean Absolute Error: {mae}")


# Function to test the model on a new image
def test_image(image_path):
    test_image = load_and_preprocess_image(image_path)
    test_image = np.expand_dims(
        test_image, axis=0
    )  # Expand dimensions to match model input shape
    severity_score = model.predict(test_image)[0][0]
    if severity_score > 0:
        label_result = "Fire detected"
    else:
        label_result = "No fire detected"
    return severity_score, label_result


# Example usage
cur = os.path.dirname(__file__)
test_image_path = os.path.join(cur, "download.jpg")
severity_score, label_result = test_image(test_image_path)
print(f"Label Prediction: {label_result}")
print(f"Predicted Severity Score: {severity_score}")
