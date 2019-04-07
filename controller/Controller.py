#!/usr/local/bin/python
# coding: utf-8

from PIL import Image

from model import FileCheck, Config, LoadImages, Model2
from model.decorators import Decorators
from view import View


@Decorators.view(View.save_final_image)
@Decorators.timer()
def save_image(final_image: Image, path: str, file_format: str = None) -> None:
	final_image.save(path, format=file_format)


@Decorators.timer(View.total_time)
def execute() -> None:

	dir_src = Config.get_default_dir()

	images_sources = FileCheck.get_dir_content(dir_src)

	View.n_images_found(len(images_sources))

	images = LoadImages.load_images_with_resize(dir_src, images_sources, Config.get_small_size(), Config.get_small_size())

	master = FileCheck.get_image(dir_src + "/" + Config.get_master_name())

	model = Model2.Modeler()\
		.set_master(master)\
		.add_images(images)\
		.set_small_size(50)\
		.set_size(100, size_type='r')\
		.set_gradient_type('mean')\
		.set_overlay(0.45)

	final_image = model.resize_all().\
		gradients().\
		links().\
		make_final()

	save_image(final_image, Config.get_save_path(), Config.get_save_format())

