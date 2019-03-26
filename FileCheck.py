#!/usr/local/bin/python
# coding: utf-8

import os
from PIL import Image


def is_valid_dir(path):
	if type(path) is str or type(path) is bytes or type(path) is os.PathLike or type(path) is int:
		return os.path.exists(path) and os.path.isdir(path)
	return False


def get_dir_content(path):
	if is_valid_dir(path):
		try:
			return os.listdir(path)
		except Exception:
			return []
	return []


def get_image(path):
	if os.path.exists(path) and os.path.isfile(path) and os.access(path, os.R_OK):
		try:
			image = Image.open(path)
			return image
		except Exception:
			return None
	return None
