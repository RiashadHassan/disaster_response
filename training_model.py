import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
)
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import VGG16
from tensorflow.keras.optimizers import Adam

# Paths to directories
fire_image_dir = r"C:\Users\WALTON\Downloads\Large-Fire\all_images"
non_fire_image_dir = r"C:\Users\WALTON\Downloads\Large-Fire\non-fire"
labels_csv = r"C:\Users\WALTON\Downloads\Large-Fire\labels.csv"

# Load existing labels CSV
labels_df = pd.read_csv(labels_csv)


# Function to add images to DataFrame
def add_images_to_df(image_dir, label, severity, df):
    rows = []
    for filename in os.listdir(image_dir):
        if (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):
            rows.append({"filename": filename, "label": label, "severity": severity})
    return pd.concat([df, pd.DataFrame(rows)], ignore_index=True)


# Add non-fire images to DataFrame
labels_df = add_images_to_df(non_fire_image_dir, label=0, severity=0, df=labels_df)

# Save updated labels CSV
updated_labels_csv = r"C:\Users\WALTON\Downloads\Large-Fire\updated_labels.csv"
labels_df.to_csv(updated_labels_csv, index=False)
print(f"Updated labels CSV file saved successfully at: {updated_labels_csv}")

# Add a column with the full path to the images
labels_df["file_path"] = labels_df.apply(
    lambda row: os.path.join(
        fire_image_dir if row["label"] == 1 else non_fire_image_dir, row["filename"]
    ),
    axis=1,
)


# Function to load and preprocess images
def load_and_preprocess_image(file_path):
    img = load_img(file_path, target_size=(64, 64))  # Using 64x64 for VGG16
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    return img_array


# Load images and labels
X = np.zeros((len(labels_df), 64, 64, 3))
y = labels_df[
    "severity"
].values  # Use severity as the label, with 0 indicating non-fire

for idx, row in labels_df.iterrows():
    file_path = row["file_path"]
    X[idx] = load_and_preprocess_image(file_path)

# Split data into training and validation sets
split = int(0.8 * len(X))  # 80% training, 20% validation
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)

# Load the VGG16 model pre-trained on ImageNet
base_model = VGG16(weights="imagenet", include_top=False, input_shape=(64, 64, 3))

# Freeze the convolutional base
for layer in base_model.layers:
    layer.trainable = False

# Add new layers for fine-tuning
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation="relu")(x)
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
test_image_path = os.path.join(cur, "car.jpg")
severity_score, label_result = test_image(test_image_path)
print(f"Label Prediction: {label_result}")
print(f"Predicted Severity Score: {severity_score}")
