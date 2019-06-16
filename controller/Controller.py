#!/usr/local/bin/python
# coding: utf-8

from PIL import Image

from model import FileCheck, Config, LoadImages, Model2
from model.decorators import Decorators
from view import ConsoleView


@Decorators.view(ConsoleView.save_final_image)
@Decorators.timer()
def save_image(final_image: Image, path: str, file_format: str = None) -> None:
    """
        Save final image in the requested path and format.
        The view is alerted with the time duration when the method is finish.
    """
    final_image.save(path, format=file_format)


@Decorators.timer(ConsoleView.total_time)
def execute() -> None:
    """
        Execute all methods and coordinates the answers.
        The view display the time duration when the method is finish.
    """
    dir_src = Config.get_default_dir()

    images_sources = FileCheck.get_dir_content(dir_src)

    ConsoleView.n_images_found(len(images_sources))

    images = LoadImages.load_images_with_resize(dir_src, images_sources, Config.get_small_size()[0], Config.get_small_size()[1])

    master = FileCheck.get_image(dir_src + "/" + Config.get_master_name())

    model = Model2.Modeler()\
        .set_master(master)\
        .add_images(images)\
        .set_small_size(Config.get_small_size())\
        .set_size(Config.get_master_size(), size_type='ri')\
        .set_gradient_type(Config.get_gradient_type())\
        .set_overlay(Config.get_overlay())

    final_image = model.resize_all().\
        gradients().\
        links().\
        make_final()

    save_image(final_image, Config.get_save_path(), Config.get_save_format())

