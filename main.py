import keras
import tensorflow as tf
import numpy as np
import imgaug.augmenters as iaa
from keras_applications.mobilenet_v3 import MobileNetV3Small

import var as v
import functions

# multi task learning - Inductive Transfer Learning
# Off-the-shelf Pre-trained Models as Feature Extractors
# Instance Segmentation - Datasets: PASCAL, COCO


if __name__ == '__main__':

    # Podział folderów z zdjęciami na zdjecia do trenowania i testowania
    # functions.make_train_split(v.split_category_list, v.split_data_path, v.split_test_size)

    # Validation, train and test split - kod w done.py

    # Tworzenie obektu klasy ImageTypeChecker
    image_checker = functions.ImageTypeChecker(v.img_extensions, v.img_type_accepted)
    # Sprawdzenie typu plików w podanym katalogu
    image_checker.img_type_accepted_by_mobilnetv3(v.data_path_to_check)

    image_checker.remove_files_with_unaccepted_extensions(v.data_path_to_check, v.img_extensions)
    # proba dopracowania mnijeszej funkcji check_file_type
    #functions.check_file_type(v.data_path_to_check, v.img_extensions, v.img_type_accepted)