import os
import random

category_list = ['koszulki', 'spodnie', 'sukienki']
data_path = r'D:\vision\data\\'
test_size = 0.2



# Funkcja służąca do podziału danych na zbór treningowy i testowy dla każdej podkategorii
def make_train_test_split(category_list, data_path, test_size):

    for subcategory in category_list:
        # Dla każdej kategorii z listy tworzy katalog test
        os.makedirs(data_path + '/test' + subcategory, exist_ok=True)
        # Sprawdzenie listy plików w katalogu train i przypisanie do zmiennej
        file_list = os.listdir(data_path + '/train' + subcategory)
        # Obliczanie liczby próbek do przeniesienia
        number_of_samples = int(len(file_list) * test_size)

    # wybiera losowo określoną liczbę próbek określaną przez zmienna number_of_samples
    for file_name in random.sample(file_list, number_of_samples):
        # przenosi plik z katalogu treningowego do testowego, zmieniając ścieżkę pliku
        os.rename(data_path + '/train/' + subcategory + '/' + file_name,
                  data_path + '/test/' + subcategory + '/' + file_name)
