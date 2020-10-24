import io
import logging
import time

from PIL import Image

logging.basicConfig(level=logging.INFO)


def worker_png(obj, w, h):
    logging.info(f'Get object with id={obj.id} in worker_png with width={w} and high={h}')
    start = time.time()
    im = Image.open(io.BytesIO(obj.picture))
    im_resized = im.resize((int(w), int(h)))

    new_filename = "data/resized.png"
    im_resized.save(new_filename, "PNG")

    logging.info(f'Save file: {new_filename}')
    logging.info(f'Time of png worker = {time.time() - start}')

    return new_filename


def worker_jpg(obj, w, h):
    logging.info(f'Get object with id={obj.id} in worker_jpg with width={w} and high={h}')
    start = time.time()
    im = Image.open(io.BytesIO(obj.picture))
    im_rgb = im.convert('RGB')
    im_resized = im_rgb.resize((int(w), int(h)))

    new_filename = "data/resized.jpeg"
    im_resized.save(new_filename, "JPEG")

    logging.info(f'Save file: {new_filename}')
    logging.info(f'Time of jpg worker = {time.time() - start}')

    return new_filename
