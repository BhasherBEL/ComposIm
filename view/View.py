#!/usr/local/bin/python
# coding: utf-8

import sys


def get_source_path() -> str:
	return input("Dossier source ? ")


def invalid_source_path(dir_path: str = None) -> None:
	if dir_path is None:
		print('Le dossier source n\'est pas un dossier valide !')
	else:
		print('{0} n\'est pas un dossier valide !'.format(dir_path))


def n_images_found(n: int) -> None:
	print("{0} images trouvées.".format(n))


def load() -> None:
	sys.stdout.write('\rChargement des images ... ')


def resize() -> None:
	sys.stdout.write('\rRedimensionnement des images ...')


def gradient() -> None:
	sys.stdout.write('\rCalcul des gradients ...')


def save() -> None:
	sys.stdout.write('\rSauvegarde des images ... ')


def link() -> None:
	sys.stdout.write('\rLiaison des pixels avec les images ... ')


def make_final() -> None:
	sys.stdout.write('\rCréation de l\'image finale ... ')


def save_final_image() -> None:
	sys.stdout.write('\rSauvegarde de l\'image finale ... ')


def ok_task(time: float = None) -> None:
	print('Ok' + ('' if time is None else ' ({}s)'.format(round(time, 2))))
