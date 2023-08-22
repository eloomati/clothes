# )

print("Tensorflow version " + tf.__version__)

try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    print('Running on TPU ', tpu.master())
except ValueError:
    tpu = None

if tpu:
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
else:
    strategy = tf.distribute.get_strategy()

print("REPLICAS: ", strategy.num_replicas_in_sync)

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
    image = tf.cast(image, tf.uint8)  # convert image to floats in [0, 255] range
    return image, label


data_path = r'D:\vision\data'
datagen = ImageDataGenerator(validation_split=0.2)
dataset = load_dataset(datagen, labeled=True)

for image, label in datagen.take(1):
    plt.figure(figsize=(10, 10))
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        augmented_image = data_augmentation(image, label)[0]
        # print(augmented_image.dtype) # uint8
        # print(augmented_image.numpy().max())
        plt.imshow(augmented_image / 255)
        plt.axis('off')