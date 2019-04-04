#!/usr/local/bin/python
# coding: utf-8

import numpy as np
import operator
from PIL import Image
import scipy
import scipy.cluster

colors = {'black': np.array([0, 0, 0]),
		  'white': np.array([255, 255, 255]),
		  'red': np.array([255, 0, 0]),
		  'green': np.array([0, 255, 0]),
		  'blue': np.array([0, 0, 255]),
		  'yellow': np.array([255, 255, 0]),
		  'cyan': np.array([0, 255, 255]),
		  'magenta': np.array([255, 0, 255]),
		  #'gray': np.array([128, 128, 128]),
		  'dark_green': np.array([0, 128, 0]),
		  'dark_cyan': np.array([0, 128, 128])}


def get_gradient(image: Image) -> np.array:
	return get_mean_gradient(image.getdata())


def get_mean_gradient(data: list) -> np.array:
	return np.array(data).mean(axis=0).astype(dtype=int)


def get_table_gradient(data: list) -> np.array:
	pts = {}
	for color in colors.keys():
		pts[color] = 0

	for pixel in data:
		for color, value in colors.items():
			pts[color] += sum((255-abs(np.array(pixel)-value))**2)/(10**9)

	return colors[max(pts.items(), key=operator.itemgetter(1))[0]]


def get_cluster_gradient(image: Image) -> np.array:
	num_clusters = 5
	ar = np.asarray(image)
	shape = ar.shape
	ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

	codes, dist = scipy.cluster.vq.kmeans(ar, num_clusters)

	vecs, dist = scipy.cluster.vq.vq(ar, codes)
	counts, bins = scipy.histogram(vecs, len(codes))

	index_max = scipy.argmax(counts)
	peak = np.array(codes[index_max]).astype(int)

	return peak


def get_present_gradient(image: Image) -> np.array:
	shape = image.shape
	pixels = image.getcolors(shape[0] * shape[1])
	sorted_pixels = sorted(pixels, key=lambda t: t[0])
	dominant_color = sorted_pixels[-1][1]
	return np.array(dominant_color)
