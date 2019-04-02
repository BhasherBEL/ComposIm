#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import numpy as np
import random
import multiprocessing
import time
import os

from view import View
from model import Gradients, FileCheck, Config

gradient_values = {}


def put_gradient(image: Image, i: int) -> None:
	q.put([i, Gradients.get_gradient(image.getdata())])


def generate(images_data: dict, master: Image, images_size: int, master_size: int) -> Image:
	global q

	pre_path = []

	post_path = []
	images = []

	for path, image in images_data.items():
		if not Config.use_memory() or image is not None:
			if Config.use_memory():
				post_path.append(path)
			images.append(image)
		else:
			pre_path.append(path)

	master_data = np.array(master.resize((master_size, master_size)).getdata())
	len_images = len(images)

	start_time = time.time()
	View.resize()
	for i in range(len_images):
		if images[i].size != (images_size, images_size):
			images[i] = images[i].resize((images_size, images_size))

	View.ok_task(time.time()-start_time)
	start_time = time.time()
	View.gradient()

	images_gradient = {}
	q = multiprocessing.Queue()
	for i in range(len_images):
		multiprocessing.Process(target=put_gradient, args=(images[i], i)).start()

	View.ok_task(time.time()-start_time)
	start_time = time.time()
	View.save()

	for i in range(len_images):
		result = q.get(True)
		images_gradient[result[0]] = result[1]

	View.ok_task(time.time()-start_time)
	start_time = time.time()
	View.link()

	gradient_last_index = len(images_gradient)-1

	path_gradients = {}
	path_images = {}

	for path in pre_path:
		try:
			images_gradient[len(images_gradient)] = gradient_values[path]
			path_gradients[len(images_gradient)-1] = path
		except ValueError as e:
			print(e)

	according = {}
	len_master_data = len(master_data)
	for i in range(len_master_data):
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

	View.ok_task(time.time()-start_time)
	start_time = time.time()
	View.make_final()

	correspondence = np.array(list(according.values())).reshape(master_size, master_size)

	final_image = Image.new('RGB', (master_size * images_size, master_size * images_size), (255, 255, 255))

	for i in range(len(correspondence)):
		for j in range(len(correspondence[0])):
			val = correspondence[i][j]
			if val <= gradient_last_index:
				image = images[val]
			else:
				if val in path_images:
					image = path_images[val]
				else:
					path_images[val] = FileCheck.get_image(path_gradients[val]).resize((images_size, images_size))
					image = path_images[val]
			final_image.paste(image, (j * images_size, i * images_size))

	View.ok_task(time.time()-start_time)

	if Config.use_memory():
		with open(os.path.abspath('model/saves/ImageGradient'), 'a+') as file:
			for i in range(gradient_last_index+1):
				file.write("{0}:{1}:{2}:{3}\n".format(post_path[i], images_gradient[i][0], images_gradient[i][1], images_gradient[i][2]))

	return final_image
