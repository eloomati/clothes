import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization

# Tworzenie instancji modelu MobileNetV3
mobilnet_model = MobileNetV3Small(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

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
num_classes = 10  # dostosuj liczbę klas do swojego problemu
model.add(Dense(num_classes, activation='softmax'))

# Kompilacja modelu
learning_rate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Wyświetlenie informacji o modelu
model.summary()
