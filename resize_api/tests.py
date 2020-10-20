import os

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from resize_api.models import Picture


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
