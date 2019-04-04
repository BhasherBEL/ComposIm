#!/usr/local/bin/python
# coding: utf-8

import time
from PIL import Image

from model import Model, FileCheck, Config, LoadImages
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

	start_time = time.time()
	View.load()
	images = LoadImages.load_images_with_resize(dir_src, images_sources, Config.get_small_size(), Config.get_small_size())

	master_image = FileCheck.get_image(dir_src + "/" + Config.get_master_name())
	View.ok_task(time.time()-start_time)

	final_image = Model.generate(images, master_image, Config.get_small_size(), Config.get_master_size())

	save_image(final_image, Config.get_save_path(), Config.get_save_format())

