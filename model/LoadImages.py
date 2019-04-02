#!/usr/local/bin/python
# coding: utf-8

import multiprocessing
import hashlib
import os
import numpy as np

from model import FileCheck, Model, Config


def __load_image_with_resize(path: str, w_size: int, h_size: int) -> None:
	q.put([FileCheck.get_image(path).resize((w_size, h_size)), path])


def load_images_with_resize(dir_src: str, paths: list, w_size: int, h_size: int) -> dict:
	global q

	paths_saved = []
	if Config.use_memory():
		with open(os.path.abspath('model/saves/ImageGradient'), 'r') as file:
			images_list = np.array([np.array(line.replace('\n', '').split(':')) for line in file.readlines()])

		for image_data in images_list:
			try:
				paths_saved.append(image_data[0])
				Model.gradient_values[image_data[0]] = np.array([int(image_data[1]), int(image_data[2]), int(image_data[3])])
			except IndexError as e:
				print(e)

	q = multiprocessing.Queue()

	for i in range(len(paths)):
		path = dir_src + "/" + paths[i]
		if not Config.use_memory() or path not in paths_saved:
			multiprocessing.Process(target=__load_image_with_resize, args=(path, w_size, h_size)).start()
		else:
			q.put([None, path])

	images_data = {}
	for i in range(len(paths)):
		values = q.get(True)
		images_data[values[1]] = values[0]

	return images_data
