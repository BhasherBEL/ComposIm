#!/usr/local/bin/python
# coding: utf-8

from PIL import Image


def overlay(image: Image, master: Image, ratio: float):
    return Image.blend(image, master.resize(image.size), ratio) if 1 >= ratio > 0 else image
