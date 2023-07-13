import keras
import tensorflow as tf
import numpy as np
import imgaug.augmenters as iaa
from keras_applications.mobilenet_v3 import MobileNetV3Small

class DataGenerator(keras.utils.Sequence):
    'Generate data for Keras'
    def __init__(self, images, labels, batch_size=64, shuffle=False, augment=False):
        self.labels = labels # array of labels
        self.images = images # array of images
        self.batch_size = batch_size # batch size
        self.shuffle = shuffle # shuffle bool
        self.augment = augment # augment data bool
        self.on_epoch_end()

    def __len__(self):
        'Number of batches per epoch'
        return int(np.floor(len(self.images) / self.batch_size))

    def on_epoch_end(self):
        'Updata indexes after each epoch'
        self.indexes = np.arange(len(self.images))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        'Generate one batch of data'
        # selects indices of data for next batch
        indexes = self.indexes[index * self.batch_size :
                               (index + 1) * self.batch_size]
        # select data and load images
        labels = np.array([self.labels[k] for k in indexes])
        images = np.array([self.images[k] for k in indexes])

        # preporess and augment data
        if self.augment == True:
            images = self.augmentor(images)

        images = images/255
        
        return images, labels

    def augmentor(self, images):
        'Apply data augmentation'
        def sometimes(aug):
            return iaa.Sometimes(0.5, aug)
        seq = iaa.Sequential([sometimes(iaa.Crop(px=(1, 16), keep_size=True)),
                              sometimes(iaa.Fliplr(0.5)),
                              sometimes(iaa.GaussianBlur(sigma=(0, 3.0)))])
        return seq.augment_image(images)

if __name__ == '__main__':
    print('ELO')