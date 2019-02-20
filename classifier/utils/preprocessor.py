import numpy as np
from scipy.misc import imread, imresize


def _imread(image_name):
    return imread(image_name)


def _imresize(image_array, size):
    return imresize(image_array, size)


def to_categorical(integer_classes, num_classes=2):
    integer_classes = np.asarray(integer_classes, dtype='int')
    num_samples = integer_classes.shape[0]
    categorical = np.zeros((num_samples, num_classes))
    categorical[np.arange(num_samples), integer_classes] = 1
    return categorical
