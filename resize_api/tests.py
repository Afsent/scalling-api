import os
import time

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from resize_api.models import Picture
from resize_api.tasks import worker_png, worker_jpg


class ImageTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.filepath = './data/pics/2.jpg'

    def test_create_image(self):
        """
        Ensure we can create a new image object.
        """
        url = 'http://localhost:8000/cat/'
        data = {'picture': open(self.filepath, 'rb')}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Picture.objects.count(), 1)

    def test_null_image(self):
        """
        Ensure we can't create a new image object.
        """
        url = 'http://localhost:8000/cat/'
        data = {'picture': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Picture.objects.count(), 0)

    def test_incorrect_pk(self):
        """
        Ensure we can't take an image with incorrect pk.
        """
        pk, size = 'a', '100X100'
        url = f'http://localhost:8000/cat/{pk}/{size}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_worker_png(self):
        """
        Ensure we can take a new file with png format.
        """
        file = open(self.filepath, 'rb')
        obj = Picture.objects.create(picture=file.read())
        w, h = "100", "100"
        filename = worker_png(obj, w, h)
        self.assertEqual(filename, "data/resized.png")
        os.remove(filename)

    def test_worker_jpg(self):
        """
        Ensure we can take a new file with jpeg format.
        """
        file = open(self.filepath, 'rb')
        obj = Picture.objects.create(picture=file.read())
        w, h = "100", "100"
        filename = worker_jpg(obj, w, h)
        self.assertEqual(filename, "data/resized.jpeg")
        os.remove(filename)

    def test_big_files(self):
        """
        Ensure we can resize big size.
        """
        url = 'http://localhost:8000/cat/'
        data = {'picture': open(self.filepath, 'rb')}
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        pk, size = 1, '10000X10000'
        url = f'http://localhost:8000/cat/{pk}/{size}'
        start = time.time()
        response = self.client.get(url)
        response_image = self.client.get(response.url)

        print(f"\nTime to get image = {time.time() - start}\n")
        self.assertEqual(response_image.status_code, status.HTTP_200_OK)
        self.assertNotEquals(response_image.status_code, status.HTTP_504_GATEWAY_TIMEOUT)
        self.assertNotEquals(response_image.status_code, status.HTTP_408_REQUEST_TIMEOUT)
