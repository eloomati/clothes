import var

import keras
import numpy as np
import imgaug.augmenters as iaa

import os
import random

from pathlib import Path
from PIL import Image
import concurrent.futures



class DataGenerator(keras.utils.Sequence):
    'Generate data for Keras'

    def __init__(self, images, labels, batch_size=64, shuffle=False, augment=False):
        self.labels = labels  # array of labels
        self.images = images  # array of images
        self.batch_size = batch_size  # batch size
        self.shuffle = shuffle  # shuffle bool
        self.augment = augment  # augment data bool
        self.on_epoch_end()

    def __len__(self):
        'Number of batches per epoch'
        return int(np.floor(len(self.images) / self.batch_size)) # oblicza ilosc batchow na epoke poprzez dzielenie liczby
                                                    # obrazów w zbiorze danych przez rozmiar batchow i zaokragla w dol

    # wywałanie ten metody po każdej epoce powoduje aktualizacje tablicy indeksów, co pozwala na wygenerowanie nowych
    # losowych batchów w kolejnej epoce (jeśli shuffle = True)
    def on_epoch_end(
            self):  # wywyływana po zakończeniu każdej epoki tren. lub test. i służy do aktualizacji indeksów danych
        'Updata indexes after each epoch'
        self.indexes = np.arange(len(self.images))  # Tworzy tablice, która zawiera numery indeksów dla wszystkich
                                # obrazów w zbiorze danych. Liczba indeksow = liczba obrazow
        if self.shuffle:
            np.random.shuffle(self.indexes)  # metoda losowo  przemieszcza indeksy (random.shuffle). Powoduje to losowe
                                            #  ustawienie kolejności obrazów w każdej epoce

    # metoda służąca do dokonywania augmentacji danych na zbiorze obrazów
    def augmentor(self, images):
        'Apply data augmentation'  # Augumentacja będzie stosowana w przypadakch gdy losowo wygenerowana liczba

        def sometimes(aug):  # jest mniejsza niż 0.5, inaczej dane zostana nie zmienione
            return iaa.Sometimes(0.5, aug)
        seq = iaa.Sequential(
            [sometimes(iaa.Crop(px=(1, 16), keep_size=True)),  # wywołanie sekwencji, zawierającej operacje
             sometimes(iaa.Fliplr(0.5)),  # augumentacji. Przycięcie (Crop),
             sometimes(iaa.GaussianBlur(sigma=(0, 3.0)))])  # odbicie lustrzane (Flipr), rozmycie gaussowskie

        return seq.augment_image(images)  # wywołanie metody augment_image na obiekcie seq i przekazanie do niej tablicy
                                        # obrazów. Zwraca zmodyfikowaną tablicę obrazów jako wynik

    # metoda wywoływana jest gdy próbujemy uzyskać dane z generatora za pomocą notacji generator[index]
    def __getitem__(self, index):
        'Generate one batch of data'
        # selects indices of data for next batch              # tworzy tablice, która zawiera numery indeksów danych dla
        indexes = self.indexes[
                  index * self.batch_size:  # batcha. Indeksy wybiera się za pomocą 'index' i rozmiaru batcha.
                  (index + 1) * self.batch_size]  # Efekt: każde wywałanie __getitem__ z innym indeksem da inny batch
        # select data and load images
        labels = np.array([self.labels[k] for k in indexes])  # wybiera etykiete odpowiadajaca indeksom (z indexes)
        images = np.array([self.images[k] for k in indexes])  # wybiera obrazy odpowiadajace indeksom (z indexes)

        # preporess and augment data
        if self.augment == True:  # dokonuje przetwarzania i augumentacji danych przy użyciu metody augmentor
            images = self.augmentor(images)

        images = images / 255  # noramlizuje wartość pikseli dzieląc przez 255, co sprowadza je od 0 do 1

        return images, labels  # zwraca znormalizowany obraz i etykiety


# Funkcja służąca do podziału danych na zbór treningowy i testowy dla każdej podkategorii
def make_train_split(split_category_list, split_data_path, split_test_size):
    os.makedirs(split_data_path + r'\test', exist_ok=True)

    for subcategory in split_category_list:
        # Dla każdej kategorii z listy tworzy katalog test
        os.makedirs(split_data_path + r'\test\\' + subcategory, exist_ok=True)
        # Sprawdzenie listy plików w katalogu train i przypisanie do zmiennej
        file_list = os.listdir(split_data_path + r'\train\\' + subcategory)
        # Obliczanie liczby próbek do przeniesienia
        number_of_samples = int(len(file_list) * split_test_size)

        # wybiera losowo określoną liczbę próbek określaną przez zmienna number_of_samples
        for file_name in random.sample(file_list, number_of_samples):
            # przenosi plik z katalogu treningowego do testowego, zmieniając ścieżkę pliku
            os.rename(split_data_path + r'\train\\' + subcategory + r'\\' + file_name,
                      split_data_path + r'\test\\' + subcategory + r'\\' + file_name)

def check_file_type(file_path, img_extensions, img_type_accepted):
    # sprawdzenie czy rozszerzenie pliku znajduje się na liście
    if file_path.suffix.lower() in img_extensions:
        # proba otworzenia pliku
        try:
            with Image.open(file_path) as img:
                # pobieranie formatu obrazu i zamiana na małe litery
                img_format = img.format.lower()
                # sprawdzenie czy format nie jest akceptowany przez Mobilnet
                if img_format not in img_type_accepted:
                    return f'{file_path} is a {img_format}, not accepted by MobilNetV3'
        # zwrocenie inforamcji o nieudanym otwarciu pliku
        except IOError:
            return f'Unable to open {file_path}'
    # zwrocenie None oznaczający akceptacje przez MobilNetV3
    return None

class ImageTypeChecker:
    def __init__(self, img_extensions, img_type_accepted):
        self.img_extensions = img_extensions
        self.img_type_accepted = img_type_accepted

    def img_type_accepted_by_mobilnetv3(self, data_path):
        # pobranie listy ścieżek do plików w katalogu
        file_paths = list(Path(data_path).rglob('*'))
        # tworzy ktory przetwarza rownolegle funkcje dla kazdej sciezki
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Wykonanie przetworzenia równoległego
            results = executor.map(
                lambda file_path: check_file_type(file_path, self.img_extensions, self.img_type_accepted),
                file_paths
            )
        # Iteracja po wynikach z results
        for result, file_path in zip(results, file_paths):
            # jesli check_file_type zwraca komunikat o nieakceptowanym formacie,
            # drukowany jest wynik, usuwany plik i odpowiendi komunikat
            if result is not None:
                print(result)
                os.remove(file_path)
                print(f'Removed file: {file_path}')

    @staticmethod
    def remove_files_with_unaccepted_extensions(data_path, img_extensions):
        for subdir, dirs, files in os.walk(data_path):
            for file_name in files:
                file_path = os.path.join(subdir, file_name)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(file_name)[1].lower()
                    if file_extension not in img_extensions:
                        os.remove(file_path)
                        print(f'Removed file: {file_path}')
