def run():
    import os
    import tensorflow as tf
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def _parse_function(proto):
        # Define your `tf.train.Feature` schema
        keys_to_features = {
            "image/encoded": tf.io.FixedLenFeature([], tf.string),
            "image/class/label": tf.io.FixedLenFeature([], tf.int64),
            # Add other features you expect in the TFRecord
        }

        # Load one example
        parsed_features = tf.io.parse_single_example(proto, keys_to_features)

        # Turn your data into the right format
        image = tf.io.decode_jpeg(parsed_features["image/encoded"])
        label = tf.cast(parsed_features["image/class/label"], tf.int32)

        # Preprocess the image (e.g., resize, normalize)
        image = tf.image.resize(image, [224, 224])
        image = image / 255.0  # normalize to [0,1] range

        return image, label

    # Function to load dataset from TFRecord files
    def load_dataset(filenames):
        # Create a dataset from the TFRecord file(s)
        dataset = tf.data.TFRecordDataset(filenames)

        # Map the parsing function over the dataset
        dataset = dataset.map(
            _parse_function, num_parallel_calls=tf.data.experimental.AUTOTUNE
        )

        return dataset

    # Function to display images from dataset
    def display_images_from_dataset(dataset, num_images):
        # Create an iterator for the dataset
        iterator = iter(dataset)

        # Display the images and labels
        for _ in range(num_images):
            image, label = next(iterator)
            plt.figure()
            plt.imshow(image.numpy())
            plt.title(f"Label: {label.numpy()}")
            plt.axis("off")
            plt.show()

        dataset = load_dataset(filenames)

        # Display the first 5 images
        display_images_from_dataset(dataset, num_images=5)
