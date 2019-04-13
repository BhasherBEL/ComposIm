#!/usr/local/bin/python
# coding: utf-8

import multiprocessing
import random
import numpy as np
from PIL import Image

from model import Gradients, Filters
from model.decorators import Decorators
from view import ConsoleView


def put_gradient(image: Image, i: int) -> None:
    q.put([i, Gradients.get_gradient(image)])


@Decorators.view(ConsoleView.resize)
@Decorators.timer()
def resize_all(images: list, w_size: int, h_size: int) -> list:
    for i in range(len(images)):
        if images[i].size != (w_size, h_size):
            images[i] = images[i].resize((w_size, h_size))
    return images


@Decorators.view(ConsoleView.gradient)
@Decorators.timer()
def multiprocess_gradients(images: list) -> None:
    global q
    q = multiprocessing.Queue()
    for i in range(len(images)):
        multiprocessing.Process(target=put_gradient, args=(images[i], i)).start()


@Decorators.view(ConsoleView.save)
@Decorators.timer()
def multiprocess_saver(len_images: int) -> dict:
    images_gradient = {}
    for i in range(len_images):
        result = q.get(True)
        images_gradient[result[0]] = result[1]
    return images_gradient


@Decorators.view(ConsoleView.link)
@Decorators.timer()
def links(master_data: list, images_gradient: dict) -> dict:
    according = {}
    for i in range(len(master_data)):
        best = []
        best_value = 195076
        for j in range(len(images_gradient)):
            value = ((master_data[i] - images_gradient[j]) ** 2).sum()
            if value <= best_value:
                best_value = ((master_data[i] - images_gradient[j]) ** 2).sum()
                if value < best_value:
                    best = [j]
                else:
                    best.append(j)

        according[i] = random.choice(best)
    return according


@Decorators.view(ConsoleView.make_final)
@Decorators.timer()
def make_final(according: dict, images: list, master_size: int, images_size: int):
    correspondence = np.array(list(according.values())).reshape(master_size, master_size)

    final_image = Image.new('RGB', (master_size * images_size, master_size * images_size), (255, 255, 255))

    for i in range(len(correspondence)):
        for j in range(len(correspondence[0])):
            final_image.paste(images[correspondence[i][j]], (j * images_size, i * images_size))

    return final_image


def generate(images: list, master: Image, images_size: int, master_size: int) -> Image:

    master_data = master.resize((master_size, master_size)).getdata()

    images = resize_all(images, images_size, images_size)

    multiprocess_gradients(images)

    images_gradient = multiprocess_saver(len(images))

    according = links(master_data, images_gradient)

    final_image = make_final(according, images, master_size, images_size)

    overlay_final_image = Filters.overlay(final_image, master, 0.45)

    return overlay_final_image
