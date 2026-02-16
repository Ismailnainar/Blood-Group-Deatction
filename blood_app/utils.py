import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from django.conf import settings
from cryptography.fernet import Fernet
import base64
import hashlib

# Define constants
IMAGE_SIZE = (64, 64)
MODEL_PATH = os.path.join(settings.BASE_DIR, 'blood_group_model.h5')

def get_classes():
    dataset_path = os.path.join(settings.BASE_DIR, 'dataset_blood_group')
    if not os.path.exists(dataset_path):
        return []
    return sorted([d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))])

def train_model():
    dataset_path = os.path.join(settings.BASE_DIR, 'dataset_blood_group')
    classes = get_classes()
    
    if not classes:
        return "Dataset not found or empty."

    print(f"Found {len(classes)} blood group classes: {classes}")
    
    data = []
    labels = []
    total_images = 0

    for label_id, label_name in enumerate(classes):
        class_path = os.path.join(dataset_path, label_name)
        images_in_class = os.listdir(class_path)
        count = len(images_in_class)
        print(f"Analyzing {label_name}: Found {count} images.")
        
        for img_name in images_in_class:
            try:
                img_path = os.path.join(class_path, img_name)
                img = cv2.imread(img_path)
                img = cv2.resize(img, IMAGE_SIZE)
                data.append(img)
                labels.append(label_id)
                total_images += 1
            except Exception as e:
                print(f"Error loading image {img_name}: {e}")

    print(f"Total dataset size: {total_images} images. Starting training...")

    data = np.array(data) / 255.0
    labels = np.array(labels)
    labels = to_categorical(labels, num_classes=len(classes))

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(len(classes), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    
    model.save(MODEL_PATH)
    return "Training completed successfully."

def predict_blood_group(image_path):
    if not os.path.exists(MODEL_PATH):
        return "Model not trained yet."
    
    model = load_model(MODEL_PATH)
    classes = get_classes()
    
    try:
        img = cv2.imread(image_path)
        img = cv2.resize(img, IMAGE_SIZE)
        img = np.expand_dims(img, axis=0) / 255.0
        
        prediction = model.predict(img)
        class_id = np.argmax(prediction)
        confidence = float(np.max(prediction))
        
        return classes[class_id], confidence
    except Exception as e:
        return str(e), 0.0

def get_crypto_key():
    # Derive a 32-byte key for Fernet from settings.SECRET_KEY
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_data(data):
    if not data: return ""
    f = Fernet(get_crypto_key())
    return f.encrypt(data.encode()).decode()

def decrypt_data(data):
    if not data: return ""
    try:
        f = Fernet(get_crypto_key())
        return f.decrypt(data.encode()).decode()
    except:
        return ""
