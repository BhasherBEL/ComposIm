#!/usr/local/bin/python
# coding: utf-8

import os
from PIL import Image
from typing import List


def is_valid_dir(path: str) -> bool:
	if type(path) is str or type(path) is bytes or type(path) is os.PathLike or type(path) is int:
		return os.path.exists(path) and os.path.isdir(path)
	else:
		return False


def get_dir_content(path: str) -> List[str]:
	if is_valid_dir(path):
		return os.listdir(path)
	else:
		return []


def get_image(path: str) -> (Image, None):
	if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK):
		image = Image.open(path)
		return image
	else:
		return None
