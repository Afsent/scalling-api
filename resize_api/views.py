import io
import os
from wsgiref.util import FileWrapper

from PIL import Image
from django.http.response import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from resize_api.tasks import get_png, get_jpg
from .serializers import PictureSerializer
from .models import Picture


class ImageResponse(ModelViewSet):
    def resize(self, request, pk, size):
        image = get_object_or_404(Picture, id=pk)

        try:
            w, h = size.lower().split('x')
        except ValueError:
            return Response({"message": "Error. Incorrect size"}, status=400)

        # send tasks to Celery
        task_png = get_png.delay(pk, w, h)
        task_jpg = get_jpg.delay(pk, w, h)

        # get path to file from Celery
        filepath_jpg = task_jpg.get(timeout=10)
        filepath_png = task_png.get(timeout=10)

        im = Image.open(io.BytesIO(image.picture))
        if im.format.lower() == 'png':
            response = HttpResponse(FileWrapper(open(filepath_jpg, 'rb')), content_type='image/jpg')
        else:
            response = HttpResponse(FileWrapper(open(filepath_png, 'rb')), content_type='image/png')

        os.remove(filepath_jpg)
        os.remove(filepath_png)

        return response


class ImageViewSet(ModelViewSet):
    serializer_class = PictureSerializer

    def hello(self, request):
        return Response({"message": 'hello'})

    def post(self, request, *args, **kwargs):
        if request.data['picture'] == '':
            return Response({'message': "Upload correct file"}, status=400)
        file = request.data['picture'].file.read()
        image = Picture.objects.create(picture=file)
        return Response({'message': f"Uploaded by id={image.id}"}, status=201)
