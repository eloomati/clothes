# link to google drive

from google.colab import drive
drive.mount('/content/drive')


import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate, BatchNormalization
from skimage import color
from tensorflow.keras.utils import Sequence
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split


# Wczytanie i przygotowanie danych treningowych
def load_data(data_folder, target_size=(256, 256)):
    images = []
    masks = []
    for filename in os.listdir(data_folder):
        if filename.endswith('.jpg'):
            image_path = os.path.join(data_folder, filename)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, target_size)  # Przeskalowanie do docelowej rozdzielczości
            images.append(image)

            # Generowanie maski na podstawie jasności pikseli
            gray_image = color.rgb2gray(image)
            mask = (gray_image > 0.1).astype(np.uint8)  # Próg jasności
            masks.append(np.expand_dims(mask, axis=-1))  # Dodanie dodatkowego wymiaru

    return np.array(images), np.array(masks)

# Przygotowanie danych treningowych
data_folder = 'drive/MyDrive/data/train/spodnie'
X_train, y_train = load_data(data_folder)


# Model U-Net
def unet_model(input_shape):
    inputs = Input(input_shape)

    conv1 = Conv2D(32, 3, activation='relu', padding='same')(inputs)
    conv1 = BatchNormalization()(conv1)
    conv1 = Conv2D(32, 3, activation='relu', padding='same')(conv1)
    conv1 = BatchNormalization()(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, 3, activation='relu', padding='same')(pool1)
    conv2 = BatchNormalization()(conv2)
    conv2 = Conv2D(64, 3, activation='relu', padding='same')(conv2)
    conv2 = BatchNormalization()(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, 3, activation='relu', padding='same')(pool2)
    conv3 = BatchNormalization()(conv3)
    conv3 = Conv2D(128, 3, activation='relu', padding='same')(conv3)
    conv3 = BatchNormalization()(conv3)

    up1 = UpSampling2D(size=(2, 2))(conv3)
    up1 = Conv2D(64, 2, activation='relu', padding='same')(up1)
    up1 = BatchNormalization()(up1)
    merge1 = Concatenate(axis=3)([conv2, up1])
    conv4 = Conv2D(64, 3, activation='relu', padding='same')(merge1)
    conv4 = BatchNormalization()(conv4)
    conv4 = Conv2D(64, 3, activation='relu', padding='same')(conv4)
    conv4 = BatchNormalization()(conv4)

    up2 = UpSampling2D(size=(2, 2))(conv4)
    up2 = Conv2D(32, 2, activation='relu', padding='same')(up2)
    up2 = BatchNormalization()(up2)
    merge2 = Concatenate(axis=3)([conv1, up2])
    conv5 = Conv2D(32, 3, activation='relu', padding='same')(merge2)
    conv5 = BatchNormalization()(conv5)
    conv5 = Conv2D(32, 3, activation='relu', padding='same')(conv5)
    conv5 = BatchNormalization()(conv5)

    outputs = Conv2D(1, 1, activation='sigmoid')(conv5)

    model = Model(inputs=inputs, outputs=outputs)
    return model


# Rozmiar wejściowy obrazu
input_shape = (256, 256, 3)


# Inicjalizacja generatora danych
class DataGenerator(Sequence):
    def __init__(self, x_set, y_set, batch_size, target_size, augmentations=None):
        self.x, self.y = x_set, y_set
        self.batch_size = batch_size
        self.target_size = target_size
        self.augmentations = augmentations
        self.indexes = np.arange(len(self.x))

    def __len__(self):
        return int(np.ceil(len(self.x) / self.batch_size))

    def __getitem__(self, index):
        start_idx = index * self.batch_size
        end_idx = (index + 1) * self.batch_size
        batch_x = self.x[start_idx:end_idx]
        batch_y = self.y[start_idx:end_idx]

        if self.augmentations:
            batch_x, batch_y = self.apply_augmentations(batch_x, batch_y)

        return batch_x, batch_y

    def apply_augmentations(self, batch_x, batch_y):
        augmented_images = []
        augmented_masks = []
        for i in range(len(batch_x)):
            aug_image = self.augmentations.random_transform(batch_x[i])
            aug_mask = self.augmentations.random_transform(batch_y[i])
            augmented_images.append(aug_image)
            augmented_masks.append(aug_mask)

        return np.array(augmented_images), np.array(augmented_masks)


# Inicjalizacja augmentacji
train_augmentations = ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=False,
    fill_mode='nearest'
)

# Podział danych na zbiór treningowy i walidacyjny
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Inicjalizacja generatora danych
batch_size = 16
target_size = (256, 256)
train_generator = DataGenerator(X_train, y_train, batch_size, target_size, augmentations=train_augmentations)
val_generator = DataGenerator(X_val, y_val, batch_size, target_size)  # Generator dla danych walidacyjnych

# Inicjalizacja modelu
model = unet_model(input_shape)
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Wczesne zatrzymanie
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# Trenowanie modelu
model.fit(train_generator, epochs=50, validation_data=val_generator, callbacks=[early_stopping])