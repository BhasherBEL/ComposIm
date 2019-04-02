#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import numpy as np
import random
import multiprocessing
import time

from view import View
from model import Gradients


def put_gradient(image: Image, i: int) -> None:
	q.put([i, Gradients.get_gradient(image.getdata())])


def generate(images: list, master: Image, images_size: int, master_size: int) -> Image:
	global q

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
			final_image.paste(images[correspondence[i][j]], (j * images_size, i * images_size))

	View.ok_task(time.time()-start_time)

	return final_image
