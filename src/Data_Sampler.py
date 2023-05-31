import math
import random


def split_data_according_to_ratio(data, ratio, do_shuffle=False):
    number_of_data_elements = len(data)
    number_of_elements_ratio = math.ceil(number_of_data_elements * (ratio / 100))
    if do_shuffle:
        random.shuffle(data)
    dataset_ratio = data[0:number_of_elements_ratio]
    dataset_rest = data[number_of_elements_ratio:]
    return dataset_ratio, dataset_rest
