#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import os
import numpy as np
import random
import sys

import FileCheck
import Gradients

DEFAULT_DIR = "/home/bhasher/Desktop/OYG"
MASTER_NAME = "0-02-05_full.jpg"
MASTER_SIZE = 100
SMALL_SIZE = 50


def request_path():
	dir_src = None
	while not FileCheck.is_valid_dir(dir_src):

		if dir_src is not None:
			print(dir_src, 'n\'est pas un dossier valide !')

		user_src = input("Dossier source ? ")

		if user_src == "":
			dir_src = DEFAULT_DIR
		elif user_src == "curr":
			dir_src = os.path.curdir
		else:
			dir_src = user_src
	return dir_src


if __name__ == "__main__":

	DIR_SRC = request_path()

	images_sources = FileCheck.get_dir_content(DIR_SRC)[:50]
	len_images_sources = len(images_sources)

	master_image = FileCheck.get_image(DIR_SRC + "/" + MASTER_NAME)

	master_image.resize((MASTER_SIZE, MASTER_SIZE)).save('/home/bhasher/Desktop/master.jpg', format='jpeg')

	master_data = np.array(master_image.resize((MASTER_SIZE, MASTER_SIZE)).getdata())

	print("{0} images trouvées.".format(len(images_sources)))
	sys.stdout.write(' ')

	images_gradient = {}
	images = {}

	for i in range(len(images_sources)):
		image = Image.open(DIR_SRC + "/" + images_sources[i]).resize((SMALL_SIZE, SMALL_SIZE))
		images[i] = image
		images_gradient[i] = Gradients.get_gradient(image.getdata())
		sys.stdout.write('\r{0}/{1}'.format(i+1, len_images_sources))

	according = {}
	for i in range(len(master_data)):
		best = []
		best_value = 195075
		for j in range(len(images_gradient)):
			value = ((master_data[i] - images_gradient[j]) ** 2).sum()
			if value <= best_value:
				best_value = ((master_data[i] - images_gradient[j]) ** 2).sum()
				if value < best_value:
					best = [j]
				else:
					best.append(j)

		according[i] = random.choice(best)

	correspondence = np.array(list(according.values())).reshape(MASTER_SIZE, MASTER_SIZE)

	final_image = Image.new('RGB', (MASTER_SIZE * SMALL_SIZE, MASTER_SIZE * SMALL_SIZE), (255, 255, 255))

	for i in range(len(correspondence)):
		for j in range(len(correspondence[0])):
			final_image.paste(images[correspondence[i][j]], (j * SMALL_SIZE, i * SMALL_SIZE))

	final_image.save("/home/bhasher/Desktop/test.jpg", format="jpeg")
