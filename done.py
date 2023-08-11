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
#Found 19157 files belonging to 3 classes.
#Using 15326 files for training.
#Found 19157 files belonging to 3 classes.
#Using 3831 files for validation.
#Found 4789 files belonging to 3 classes.
#Using 2395 files for training.
#Using 2394 files for validation.