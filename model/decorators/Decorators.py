#!/usr/local/bin/python
# coding: utf-8

import time

from view import View


def timer(viewer: View = None) -> classmethod:
	def decorator(fct: classmethod) -> classmethod:
		def final_function(*unnamed_parameters, **named_parameters) -> (any, float):
			pre_time = time.time()
			result = fct(*unnamed_parameters, **named_parameters)
			total_time = time.time() - pre_time

			if viewer is None:
				final_function.decorated = True
				return result, total_time
			else:
				viewer(total_time)
				return result
		return final_function
	return decorator


def view(viewer: View) -> classmethod:
	def decorator(fct: classmethod) -> classmethod:
		def final_function(*unnamed_parameters, **named_parameters) -> any:
			viewer()
			result = fct(*unnamed_parameters, **named_parameters)
			if hasattr(fct, 'decorated'):
				View.ok_task(result[1])
				return result[0]
			else:
				View.ok_task()
				return result
		return final_function
	return decorator