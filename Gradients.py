import numpy as np
import operator

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


def get_gradient(data):
	return get_mean_gradient(data)


def get_mean_gradient(data):
	return np.array(data).mean(axis=0).astype(dtype=int)


def get_table_gradient(data):
	pts = {}
	for color in colors.keys():
		pts[color] = 0

	for pixel in data:
		for color, value in colors.items():
			pts[color] += sum((255-abs(np.array(pixel)-value))**2)/(10**9)

	return colors[max(pts.items(), key=operator.itemgetter(1))[0]]
