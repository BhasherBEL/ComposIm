#!/usr/local/bin/python
# coding: utf-8

import time

from view import ConsoleView


def timer(viewer: ConsoleView = None) -> classmethod:
    """
        Get parameter of the decorator.
        :param viewer: Optional parameter to send time duration to it.
        :return the timer decorator.
    """
    def decorator(fct: classmethod) -> classmethod:
        """
            The decorator.
            :param fct: The method called with the decorator.
            :return The final function.
        """
        def final_function(*unnamed_parameters, **named_parameters) -> (any, float):
            """
                Calculate the duration of the fct method.
                :return The result of the fct method and optionally the time duration.
            """
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


def view(viewer: ConsoleView) -> classmethod:
    def decorator(fct: classmethod) -> classmethod:
        def final_function(*unnamed_parameters, **named_parameters) -> any:
            viewer()
            result = fct(*unnamed_parameters, **named_parameters)
            if hasattr(fct, 'decorated'):
                ConsoleView.ok_task(result[1])
                return result[0]
            else:
                ConsoleView.ok_task()
                return result
        return final_function
    return decorator
