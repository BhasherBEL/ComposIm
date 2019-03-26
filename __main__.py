#!/usr/local/bin/python
# coding: utf-8

from PIL import Image
import os
import numpy as np
import random
import sys
import multiprocessing
import copy

import FileCheck
import Gradients

DEFAULT_DIR = "/home/bhasher/Desktop/OYG"
MASTER_NAME = "0-02-05_full.jpg"
MASTER_SIZE = 150
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


def generate(path, i):
	image = Image.open(path).resize((SMALL_SIZE, SMALL_SIZE))
	q.put([image, Gradients.get_gradient(image.getdata()), i])


if __name__ == "__main__":

	DIR_SRC = request_path()

	images_sources = FileCheck.get_dir_content(DIR_SRC)
	len_images_sources = len(images_sources)

	master_image = FileCheck.get_image(DIR_SRC + "/" + MASTER_NAME)

	master_image.resize((MASTER_SIZE, MASTER_SIZE)).save('/home/bhasher/Desktop/master.jpg', format='jpeg')

	master_data = np.array(master_image.resize((MASTER_SIZE, MASTER_SIZE)).getdata())

	print("{0} images trouvées.".format(len_images_sources))
	sys.stdout.write(' ')

	images_gradient = {}
	images = {}
	q = multiprocessing.Queue()

	for i in range(len_images_sources):
		multiprocessing.Process(target=generate, args=(DIR_SRC + "/" + images_sources[i], i)).start()
		if (i+1) % 20 == 0:
			sys.stdout.write('\rChargement ... {0}/{1}'.format(i+1, len_images_sources))

	sys.stdout.write('\rChargement ... {0}/{0} Ok'.format(len_images_sources))
	print(' ')
	for i in range(len_images_sources):
		result = q.get(True)
		images[result[2]] = result[0]
		images_gradient[result[2]] = result[1]
		if (i+1) % 20 == 0:
			sys.stdout.write('\rSauvegarde ... {0}/{1}'.format(i+1, len_images_sources))

	sys.stdout.write('\rSauvegarde ... {0}/{0} Ok'.format(len_images_sources))
	print(' ')

	according = {}
	len_master_data = len(master_data)
	for i in range(len_master_data):
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
		if (i+1) % 200 == 0:
			sys.stdout.write('\rLien ... {0}/{1}'.format(i+1, len_master_data))

		according[i] = random.choice(best)

	sys.stdout.write('\rLien ... {0}/{0} Ok'.format(len_master_data))
	print(' ')

	correspondence = np.array(list(according.values())).reshape(MASTER_SIZE, MASTER_SIZE)

	sys.stdout.write('\rCréation de l\'image finale ...')

	final_image = Image.new('RGB', (MASTER_SIZE * SMALL_SIZE, MASTER_SIZE * SMALL_SIZE), (255, 255, 255))

	for i in range(len(correspondence)):
		for j in range(len(correspondence[0])):
			final_image.paste(images[correspondence[i][j]], (j * SMALL_SIZE, i * SMALL_SIZE))

	sys.stdout.write('\rCréation de l\'image finale ... Ok')
	print(' ')
	sys.stdout.write('\rSauvegarde de l\'image finale ...')

	final_image.save("/home/bhasher/Desktop/test.jpg", format="jpeg")
	sys.stdout.write('\rSauvegarde de l\'image finale ... Ok')
