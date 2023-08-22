import keras
import numpy as np
import imgaug.augmenters as iaa

class DataGenerator(keras.utils.Sequence):
  'Generates data for Keras'
  def __init__(self, images, labels, batch_size=64, shuffle=False, augment=False):
    self.labels = labels                    # array of labels
    self.images = images                    # array of images
    self.batch_size = batch_size            # batch size
    self.shuffle = shuffle                  # shuffle bool
    self.augment = augment                  # augment data bool
    self.on_epoch_end()

  # oblicza ilosc batchow na epoke poprzez dzielenie liczby
  # obrazów w zbiorze danych przez rozmiar batchow i zaokragla w dol
  def __len__(self):
    'Denotes the number of batches per epoch'
    return int(np.floor(len(self.images) / self.batch_size))


  # wywałanie ten metody po każdej epoce powoduje aktualizacje tablicy indeksów,
  # co pozwala na wygenerowanie nowych losowych batchów w kolejnej epoce
  # (jeśli shuffle = True)
  def on_epoch_end(self):
    'Updates indexes after each epoch'
    # Tworzy tablice, która zawiera numery indeksów dla wszystkich
    # obrazów w zbiorze danych. Liczba indeksow = liczba obrazow
    self.indexes = np.arange(len(self.images))
    # metoda losowo  przemieszcza indeksy (random.shuffle). Powoduje to losowe
    # ustawienie kolejności obrazów w każdej epoce
    if self.shuffle:
      np.random.shuffle(self.indexes)

  # metoda służąca do dokonywania augmentacji danych na zbiorze obrazów
  def augmentor(self, images):
    'Apply data augmentation'
    # Augumentacja będzie stosowana w przypadakch gdy losowo wygenerowana liczba
    # jest mniejsza niż 0.5, inaczej dane zostana nie zmienione
    def sometimes(aug):
      return iaa.Sometimes(0.5, aug)
    # wywołanie sekwencji, zawierającej operacje augumentacji.
    # Przyciecie (Crop), odbicie lustrzane (Flipr), rozmycie Gausowskie
    seq = iaa.Sequential([sometimes(iaa.Crop(px=(1, 16), keep_size=True)),
                         sometimes(iaa.Fliplr(0.5)),
                         sometimes(iaa.GaussianBlur(sigma=(0, 3.0)))])
    # Zwraca zmodyfikowaną tablicę obrazów jako wynik
    return seq.augment_images(images)

  # metoda wywoływana jest gdy próbujemy uzyskać dane z generatora za
  # pomocą notacji generator[index]
  def __getitem__(self, index):
    'Generate one batch of data'
    # selects indices of data for next batch
    #------------------------------------------------
    # tworzy tablice, która zawiera numery indeksów danych dla batcha.
    # Indeksy wybiera się za pomocą 'index' i rozmiaru batcha.
    # Efekt: każde wywałanie __getitem__ z innym indeksem da inny batch
    indexes = self.indexes[index * self.batch_size :
                          (index + 1) * self.batch_size]

    # select data and load images
    # ----------------------------------------------
    # wybiera etykiete odpowiadajaca indeksom (z indexes)
    labels = np.array([self.labels[k] for k in indexes])
    # wybiera obrazy odpowiadajace indeksom (z indexes)
    images = np.array([self.images[k] for k in indexes])


    # preprocess and augment data
    # ---------------------------------------------
    # dokonuje przetwarzania i augumentacji danych przy użyciu metody augmentor
    if self.augment == True:
      images = self.augmentor(images)

    # noramlizuje wartość pikseli dzieląc przez 255, co sprowadza je od 0 do 1
    images=images/255

    # zwraca znormalizowany obraz i etykiety
    return images, labels

  def real_split():
    # Train split
    train_ds = keras.utils.image_dataset_from_directory(
      v.data_path + '/train',  # scieżka do folderu zawierającego dane
      labels='inferred',  # etykiety oznaczanae na podstawie struktury folderów
      validation_split=0.2,  # procentowy udział danych do walidacji
      seed=110,
      subset='training',  # wskazuje, że otrzymujemy podzbiór treningowy danych
      image_size=(v.img_height, v.img_width),  # rozmiar do jakiego zdjęcia mają zostać przeskalowane
      batch_size=v.batch_size,  # określenie partii danych użytych do treningu
      label_mode='categorical'  # Etykiety kodowane jako kategoryczne
    )

    # Przypisanie danych trenujących
    train_images = []
    train_labels = []

    for images, labels in train_ds:
      train_images.append(images)
      train_labels.append(labels)

    # Konwersja list na numpy arrays
    train_images = np.concatenate(train_images)
    train_labels = np.concatenate(train_labels)

    # Validation split
    val_ds = keras.utils.image_dataset_from_directory(
      v.data_path + '/train',
      labels='inferred',
      validation_split=0.2,
      seed=110,
      subset='validation',
      image_size=(v.img_height, v.img_width),
      batch_size=v.batch_size,
      label_mode='categorical'
    )

    # Przypisanie danych walidacyjnych
    val_images = []
    val_labels = []

    for images, labels in val_ds:
      val_images.append(images)
      val_labels.append(labels)

    # Konwersja list na numpy arrays
    val_images = np.concatenate(train_images)
    val_labels = np.concatenate(train_labels)

    # Test split
    test_ds = keras.utils.image_dataset_from_directory(
      v.data_path + '/test',
      labels='inferred',
      validation_split=0.5,
      seed=110,
      subset='both',
      image_size=(v.img_height, v.img_width),
      batch_size=v.batch_size,
      label_mode='categorical'
    )

    # Przypisanie danych testowych
    test_images = []
    test_labels = []

    for images, labels in test_ds:
      test_images.append(images)
      test_labels.append(labels)

    # Konwersja list na numpy arrays
    test_images = np.concatenate(test_images)
    test_labels = np.concatenate(test_labels)

    return train_images, train_labels, val_images, val_labels, test_images, test_labels

# Create a generator
RNG = tf.random.Generator.from_seed(123, alg='philox')

def data_augmentation(image, label):
    # Thanks to the dataset.prefetch(AUTO)
    # statement in the next function (below), this happens essentially
    # for free on TPU. Data pipeline code is executed on the "CPU"
    # part of the TPU while the TPU itself is computing gradients.
    seed = RNG.make_seeds(2)[0]
    image = tf.image.stateless_random_flip_left_right(image, seed)
    image = tf.image.stateless_random_flip_up_down(image, seed)
    image = tf.image.stateless_random_brightness(image, 0.2, seed)
    image = tf.image.stateless_random_saturation(image, 0.5, 1.5, seed)
    image = tf.cast(image, tf.uint8) # convert image to floats in [0, 255] range
    return image, label