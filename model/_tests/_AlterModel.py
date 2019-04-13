#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import numpy as np

from model import Config, FileCheck, LoadImages, Model


def generate(master: Image, master_size: int, small_size: int) -> Image:

    dir_src = Config.get_default_dir()

    images_sources = FileCheck.get_dir_content(dir_src)

    images = LoadImages.load_images_with_resize(dir_src, images_sources, small_size, small_size)

    master_w, master_h = master.size

    if master_w > master_h:
        master_w = master_h
    elif master_h > master_w:
        master_h = master_w

    master_h -= master_h % master_size
    master_w = master_h

    master.resize((master_w, master_h))

    part_size = master_w//master_size

    master_parts = {}

    for i in range(master_size):
        if i not in master_parts:
            master_parts[i] = {}
        for j in range(master_size):
            master_parts[i][j] = np.array(master.crop((part_size*i, part_size*j, part_size*(i+1), part_size*(j+1))).getdata())

    images_reduce = {}

    for small_image in Model.resize_all(images.copy(), part_size, part_size):
        images_reduce[len(images_reduce)] = np.array(small_image.getdata())

    links = {}

    for i, line in master_parts.items():
        for j, sub_image in line.items():
            best_value = 195075 * part_size * part_size + 1
            best_id = None
            for k, small_image in images_reduce.items():
                value = ((sub_image - small_image)**2).sum()
                if value < best_value:
                    best_value = value
                    best_id = k
            links[i*master_size+j] = best_id

    Model.make_final(links, images, master_size, small_size).rotate(-90).save(Config.get_save_path())
