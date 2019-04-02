#!/usr/local/bin/python
# coding: utf-8

import time

from model import Model, FileCheck, Config, LoadImages
from view import View


def request_path() -> str:
	dir_src = None
	while not FileCheck.is_valid_dir(dir_src):

		if dir_src is not None:
			View.invalid_source_path(dir_src)

		user_src = View.get_source_path()

		if user_src == "":
			dir_src = Config.get_default_dir()
		else:
			dir_src = user_src

	return dir_src


def execute() -> None:

	dir_src = request_path()

	images_sources = FileCheck.get_dir_content(dir_src)

	View.n_images_found(len(images_sources))

	start_time = time.time()
	View.load()
	images_data = LoadImages.load_images_with_resize(dir_src, images_sources, Config.get_small_size(), Config.get_small_size())

	master_image = FileCheck.get_image(dir_src + "/" + Config.get_master_name())
	View.ok_task(time.time()-start_time)

	final_image = Model.generate(images_data, master_image, Config.get_small_size(), Config.get_master_size())

	View.save_final_image()

	final_image.save(Config.get_save_path(), format=Config.get_save_format())
	View.ok_task()
