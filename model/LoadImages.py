from model import FileCheck
import multiprocessing


def __load_image_with_resize(path: str, w_size: int, h_size: int) -> None:
	q.put(FileCheck.get_image(path).resize((w_size, h_size)))


def load_images_with_resize(dir_src: str, paths: list, w_size: int, h_size: int) -> list:
	global q

	q = multiprocessing.Queue()

	for i in range(len(paths)):
		multiprocessing.Process(target=__load_image_with_resize, args=(dir_src + "/" + paths[i], w_size, h_size)).start()

	images = []
	for i in range(len(paths)):
		images.append(q.get(True))

	return images
