import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import keras

# Ścieżka do folderu z danymi
data_dir = r'D:\vision\data'

# Wymiary obrazów
img_height = 224
img_width = 224

# Tworzenie instancji modelu MobileNetV3
mobilnet_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(img_height, img_width, 3))

# Tworzenie modelu sekwencyjnego
model = Sequential()

# Dodawanie warstw modelu MobileNetV3
model.add(mobilnet_model)

# Dodawanie warstw do modelu niestandardowego
model.add(GlobalAveragePooling2D())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(BatchNormalization())

# Warstwa wyjściowa z odpowiednią ilością klas
num_classes = 3  # dostosuj liczbę klas do swojego problemu
model.add(Dense(num_classes, activation='softmax'))

# Kompilacja modelu
learning_rate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Przygotowanie generatora danych
batch_size = 32  # liczba obrazów w jednej iteracji
datagen = ImageDataGenerator(rescale=1.0/255.0)  # Przeskalowanie pikseli do wartości [0, 1]

# Wczytanie danych z folderu
train_generator = datagen.flow_from_directory(
    data_dir + '/train',
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

# Wczytanie danych dla zbioru walidacyjnego
val_generator = datagen.flow_from_directory(
    data_dir + '/test',  # Ścieżka do folderu z danymi walidacyjnymi
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

es = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Wczytywanie danych do trenowania
history = model.fit(
    train_generator,
    epochs=10,  # dostosuj liczbę epok
    steps_per_epoch=len(train_generator),
    validation_data=val_generator,  # Dodanie zbioru walidacyjnego
    validation_steps=len(val_generator),
    verbose=1,
    callbacks=[es])

#
# Found 19157 images belonging to 3 classes.
# Found 4789 images belonging to 3 classes.
# Epoch 1/10
# 599/599 [==============================] - 658s 1s/step - loss: 0.0718 - accuracy: 0.9757 - val_loss: 1.1889 - val_accuracy: 0.3387
# Epoch 2/10
# 599/599 [==============================] - 628s 1s/step - loss: 0.0253 - accuracy: 0.9917 - val_loss: 1.3697 - val_accuracy: 0.4043
# Epoch 3/10
# 599/599 [==============================] - 639s 1s/step - loss: 0.0262 - accuracy: 0.9919 - val_loss: 5.8131 - val_accuracy: 0.2053