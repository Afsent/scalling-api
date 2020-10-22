import io
import os
import concurrent.futures
from wsgiref.util import FileWrapper

from PIL import Image
from django.http.response import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from resize_api.tasks import worker_png, worker_jpg
from .serializers import PictureSerializer
from .models import Picture
import logging

logging.basicConfig(level=logging.INFO)


class ImageResponse(ModelViewSet):
    def resize(self, request, pk, size):
        image = get_object_or_404(Picture, id=pk)

        try:
            w, h = size.lower().split('x')
        except ValueError:
            logging.error('Incorrect size in request')
            return Response({"message": "Error. Incorrect size"}, status=400)

        with concurrent.futures.ThreadPoolExecutor(2) as executor:
            future_png = executor.submit(worker_png, image, w, h)
            future_jpg = executor.submit(worker_jpg, image, w, h)

            return_value_png = future_png.result()
            return_value_jpg = future_jpg.result()

        im = Image.open(io.BytesIO(image.picture))
        if im.format.lower() == 'png':
            response = HttpResponse(FileWrapper(open(return_value_jpg, 'rb')), content_type='image/jpg')
            logging.info('Send jpg file')
        else:
            response = HttpResponse(FileWrapper(open(return_value_png, 'rb')), content_type='image/png')
            logging.info('Send png file')

        os.remove(return_value_jpg)
        os.remove(return_value_png)
        logging.info('Remove temporary files')

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
