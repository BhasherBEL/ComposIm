#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import multiprocessing
import numpy as np
import random

from model import Filters, Gradients
from view import View
from model.decorators import Decorators


def put_gradient(image: Image, i: int) -> None:
	q.put([i, Gradients.get_gradient(image)])


@Decorators.view(View.resize)
@Decorators.timer()
def resize_all(images: list, w_size: int, h_size: int) -> list:
	for i in range(len(images)):
		if images[i].size != (w_size, h_size):
			images[i] = images[i].resize((w_size, h_size))
	return images


@Decorators.view(View.gradient)
@Decorators.timer()
def multiprocess_gradients(images: list) -> None:
	global q
	q = multiprocessing.Queue()
	for i in range(len(images)):
		multiprocessing.Process(target=put_gradient, args=(images[i], i)).start()


@Decorators.view(View.save)
@Decorators.timer()
def multiprocess_saver(len_images: int) -> dict:
	images_gradient = {}
	for i in range(len_images):
		result = q.get(True)
		images_gradient[result[0]] = result[1]
	return images_gradient


@Decorators.view(View.link)
@Decorators.timer()
def links(master_data: list, images_gradient: dict) -> dict:
	according = {}
	for i in range(len(master_data)):
		best = []
		best_value = 195076
		for j in range(len(images_gradient)):
			value = ((np.array(master_data[i]) - np.array(images_gradient[j])) ** 2).sum()
			if value <= best_value:
				if value < best_value:
					best = [j]
					best_value = value
				else:
					best.append(j)

		according[i] = random.choice(best)
	return according


@Decorators.view(View.make_final)
@Decorators.timer()
def make_final(according: dict, images: list, master_w: int, master_h: int, images_space: int):
	correspondence = np.array(list(according.values())).reshape(master_h, master_w)

	final_image = Image.new('RGB', (images_space * master_w, images_space * master_h), (255, 255, 255))

	for i in range(master_h):
		for j in range(master_w):
			final_image.paste(images[correspondence[i][j]], (j * images_space, i * images_space))

	return final_image


class Modeler:

	def __init__(self) -> None:
		self.master = None
		self.images = []
		self.small_size = None
		self.gradient_type = 'mean'
		self.overlay = 0
		self.w = None
		self.h = None

	def set_master(self, master: Image) -> 'Modeler':
		self.master = master
		return self

	def set_small_size(self, size: int) -> 'Modeler':
		self.small_size = size
		return self

	def add_image(self, image: Image) -> 'Modeler':
		self.images.append(image)
		return self

	def add_images(self, images: list) -> 'Modeler':
		self.images += images
		return self

	def set_size(self, w: int, h: int = None, size_type: str = None) -> 'Modeler':
		if h is not None:
			self.w = w
			self.h = h
		elif h is None and size_type is None:
			self.w = w
			self.h = w
		elif h is None and size_type == 'r':
			if self.master is None:
				raise ValueError('Master is not define')

			master_w, master_h = self.master.size
			if master_w == master_h:
				self.w = w
				self.h = w
			elif master_w > master_h:
				self.w = int(w)
				self.h = int(self.w * master_h/master_w)
			else:
				self.h = int(w - (w % self.small_size))
				self.w = int(self.h * master_w/master_h)
		elif h is None and size_type == 'ri':
			if self.master is None:
				raise ValueError('Master is not define')

			master_w, master_h = self.master.size
			if master_w == master_h:
				self.w = w
				self.h = w
			elif master_w > master_h:
				self.h = int(w)
				self.w = int(self.h * master_w/master_h)
			else:
				self.w = int(w - (w % self.small_size))
				self.h = int(self.w * master_h/master_w)
		else:
			ValueError('Arguments are not compatibles')
		return self

	def set_gradient_type(self, gradient_type: str) -> 'Modeler':
		self.gradient_type = gradient_type
		return self

	def set_overlay(self, overlay: float) -> 'Modeler':
		self.overlay = overlay
		return self

	def make(self):

		if self.w is None or self.h is None:
			raise ValueError('Size not define')
		elif self.small_size is None:
			raise ValueError('Small size not define')
		elif not self.images:
			raise ValueError('No images set')
		elif self.master is None:
			raise ValueError('No master image')

		master_data = self.master.resize((self.w, self.h)).getdata()

		images = resize_all(self.images, self.small_size, self.small_size)

		multiprocess_gradients(images)

		images_gradient = multiprocess_saver(len(images))

		according = links(master_data, images_gradient)

		final_image = make_final(according, images, self.w, self.h, self.small_size)

		overlay_final_image = Filters.overlay(final_image, self.master, self.overlay)

		return overlay_final_image

