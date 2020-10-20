import io

from PIL import Image

from resize_api.models import Picture
from resize_pics import celery_app


@celery_app.task()
def adding_task(x, y):
    return x + y


@celery_app.task
def get_png(pk, w, h):
    obj = Picture.objects.get(id=pk)
    im = Image.open(io.BytesIO(obj.picture))
    im_resized = im.resize((int(w), int(h)))
    new_filename = "media/" + "resized.png"
    im_resized.save(new_filename, "PNG")
    return new_filename


@celery_app.task
def get_jpg(pk, w, h):
    obj = Picture.objects.get(id=pk)
    im = Image.open(io.BytesIO(obj.picture))
    im_resized = im.resize((int(w), int(h)))
    new_filename = "media/" + "resized.jpeg"
    im_resized.save(new_filename, "JPEG")
    return new_filename
