#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import multiprocessing
import numpy as np
import random

from model import Filters, Gradients
from view import View
from model.decorators import Decorators


class Modeler:

	def __init__(self) -> None:
		self.master = None
		self.images = []
		self.small_size = None
		self.gradient_type = 'mean'
		self.overlay = 0
		self.w = None
		self.h = None
		self.images_gradient = None
		self.according = None

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

	@Decorators.view(View.resize)
	@Decorators.timer()
	def resize_all(self) -> 'Modeler':
		for i in range(len(self.images)):
			if self.images[i].size != (self.small_size, self.small_size):
				self.images[i] = self.images[i].resize((self.small_size, self.small_size))
		return self

	def gradients(self) -> 'Modeler':

		q = multiprocessing.Queue()
		images_gradient = {}

		def put_gradient(image: Image, i: int) -> None:
			q.put([i, Gradients.get_gradient(image)])

		@Decorators.view(View.gradient)
		@Decorators.timer()
		def multiprocess_gradients() -> None:
			for i in range(len(self.images)):
				multiprocessing.Process(target=put_gradient, args=(self.images[i], i)).start()

		@Decorators.view(View.save)
		@Decorators.timer()
		def multiprocess_saver() -> None:
			for i in range(len(self.images)):
				result = q.get(True)
				images_gradient[result[0]] = result[1]

		multiprocess_gradients()
		multiprocess_saver()
		self.images_gradient = images_gradient
		return self

	@Decorators.view(View.link)
	@Decorators.timer()
	def links(self) -> 'Modeler':
		master_data = self.master.resize((self.w, self.h)).getdata()
		according = {}

		for i in range(len(master_data)):
			best = []
			best_value = 195076
			for j in range(len(self.images_gradient)):
				value = ((np.array(master_data[i])[:3] - np.array(self.images_gradient[j])[:3]) ** 2).sum()
				if value <= best_value:
					if value < best_value:
						best = [j]
						best_value = value
					else:
						best.append(j)

			according[i] = random.choice(best)
		self.according = according
		return self

	@Decorators.view(View.make_final)
	@Decorators.timer()
	def make_final(self) -> Image:
		correspondence = np.array(list(self.according.values())).reshape(self.h, self.w)

		final_image = Image.new('RGB', (self.small_size * self.w, self.small_size * self.h), (255, 255, 255))

		for i in range(self.h):
			for j in range(self.w):
				final_image.paste(self.images[correspondence[i][j]], (j * self.small_size, i * self.small_size))

		final_image = Filters.overlay(final_image, self.master, self.overlay)

		return final_image
