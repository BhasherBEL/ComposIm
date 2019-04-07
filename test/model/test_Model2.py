#!/usr/local/bin/python
# coding: utf-8

import unittest
from PIL import Image

from model import Model2


class TestResizeAll(unittest.TestCase):

	def test_resize_all_same(self) -> None:
		blank_images = [Image.new('RGB', (142, 189)), Image.new('RGB', (100, 100)), Image.new('RGB', (195, 9))]
		resize_images = Model2.resize_all(blank_images, 50, 50)
		for resize_image in resize_images:
			self.assertEqual(resize_image.size, (50, 50))

	def test_resize_all_different(self) -> None:
		blank_images = [Image.new('RGB', (142, 189)), Image.new('RGB', (100, 100)), Image.new('RGB', (195, 9))]
		resize_images = Model2.resize_all(blank_images, 50, 74)
		for resize_image in resize_images:
			self.assertEqual(resize_image.size, (50, 74))

	def test_resize_all_not_an_image(self) -> None:
		blank_images = ['test']
		with self.assertRaises(Exception):
			Model2.resize_all(blank_images, 50, 74)

	def test_resize_all_only_an_image(self) -> None:
		blank_image = Image.new('RGB', (142, 189))
		with self.assertRaises(Exception):
			Model2.resize_all(blank_image, 50, 50)

	def test_resize_all_zero(self) -> None:
		blank_images = [Image.new('RGB', (142, 189)), Image.new('RGB', (100, 100)), Image.new('RGB', (195, 9))]
		with self.assertRaises(ValueError):
			Model2.resize_all(blank_images, 0, 0)


class TestLinks(unittest.TestCase):

	def test_links_normal(self) -> None:
		master_data = [[0, 0, 0], [100, 100, 100], [100, 0, 200]]
		images_gradient = {0: [5, 5, 5], 1: [95, 7, 255], 2: [100, 100, 100]}
		output = Model2.links(master_data, images_gradient)
		planned_output = {0: 0, 1: 2, 2: 1}

		self.assertEqual(output, planned_output)


class TestMakeFinal(unittest.TestCase):

	according = {0: 0, 1: 2, 2: 1, 3: 0}

	master_w, master_h = (2, 2)
	images_space = 5

	images = [
		Image.new('RGB', (5, 5), (255, 0, 0)),
		Image.new('RGB', (5, 5), (0, 255, 0)),
		Image.new('RGB', (5, 5), (0, 0, 255)),
		Image.new('RGB', (5, 5), (255, 255, 255)),
	]

	planned_output = Image.new('RGB', (10, 10), (255, 255, 255))
	planned_output.paste(images[0], (0, 0))
	planned_output.paste(images[1], (0, 5))
	planned_output.paste(images[2], (5, 0))
	planned_output.paste(images[0], (5, 5))

	def test_make_final_normal(self) -> None:
		output = Model2.make_final(self.according, self.images[:3], self.master_w, self.master_h, self.images_space)
		self.assertEqual(output, self.planned_output)

	def test_make_final_out_of_range_images(self) -> None:
		with self.assertRaises(IndexError):
			Model2.make_final(self.according, self.images[:2], self.master_w, self.master_h, self.images_space)

	def test_make_final_image_not_used(self) -> None:
		output = Model2.make_final(self.according, self.images, self.master_w, self.master_h, self.images_space)
		self.assertEqual(output, self.planned_output)

	def test_make_final_size_zero(self) -> None:
		with self.assertRaises(ValueError):
			Model2.make_final(self.according, self.images[:2], 0, 0, self.images_space)


class TestModeller(unittest.TestCase):
	pass
